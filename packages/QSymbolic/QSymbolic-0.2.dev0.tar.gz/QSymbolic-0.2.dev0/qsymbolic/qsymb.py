'''
qsymb: new version of qsym
'''
from sympy import *
import itertools as itr
import numpy as np
import neal
'''
dependencies: sympy, itrtools, numpy
'''
class qsymaqc:
    '''
    object of symbolic quantum computing to solve by 
    AQC(adiabatic quantum computing). Processing flow depend on variable type
        's': the values of variables are {-1,+1}
                    H_string -> Hks-> Hkq -> H2q -> H2s->s_sol
        'q': the values variables are {0,1}
                    H_string -> Hkq->H2q -> H2s-> s_sol -> q_sol
    '''
    def __init__(self):
        # a blank string of problem hamiltonian
        self.EQ = ''
        # number of sweeps in SA
        self.NSWEEPS=1*5*10*10*1000  
        # number of rads in SA
        self.NREADS=10
        # output all configurations
        self.configurations=[]
        # output all energies
        self.energies=[]
        # output minimum configurations
        self.min_configuration=[]
        # output minimum energy
        self. min_energy=0
        # b values in Ising equation
        self.b=0
        # list of original variables
        self.var_original=[]
        # list of standardized variables
        self.var_standard=[]
        self.var_type='s'
        self.err_code=0
        # k-body --> 2-body substitution parameters
        self.delta=100
    #
    def solve(self):
        Ekx=eqString2Symbolic(self.EQ)
        #print(self.H)
        print('problem in symbolic format',Ekx)
        # assume EQ is in text with s-variable
        #
        if (self.var_type.upper()=='S'):
            '''
            ######################################################
            '''            
            print('Problem with a type-s (spin -1,+1) variable');
            varOrg,varStd,Eks = eq_standardized(Ekx,'s')
            #
            self.var_original=varOrg
            self.var_standard=varStd
            print('problem in symbolic standard format',Eks)
            # remove squared variables
            #Hks=simplifySquare(Eks) #
            Hks=simplify_squares(Eks)
            print('Hks->',Hks)
            # k-body to 2-body conversion, assume that k-max is 4
            #H2s =booleReduce(Hks)
            Hkq=Hks2Hkq(Hks)
            H2q =boole_reduce(Hkq,self.delta)
            H2s=Hkq2Hks(H2q)
            #
            # solve the problem
            print('Obtaining Ising coefficients ...')
            b, hi, Jij = get_ising_coeffs(H2s)
            maxCoeff=np.max([np.max(abs(hi)), np.max(abs(Jij))])
            #
            hi=hi/maxCoeff
            Jij=Jij/maxCoeff
            #
            b=b/maxCoeff
            # put hi in the diagonal forms of Jij
            # conform with neal data format ->J
            h, J=embed_ising_coeffs(hi, Jij)
            
            '''
            -----------------------------------------------------------------------------
            4. SOLVE THE PROBLEM
            -----------------------------------------------------------------------------
            select a solver
            > dimod: ExaxtSolver
            > neal:  SimulatedAnnealingSampler
            '''
            #
            print('Solving the problem using neal  ...')
            solver=neal.SimulatedAnnealingSampler()
            response = solver.sample_ising(h, J, sweeps=self.NSWEEPS, \
                                           num_reads=self.NREADS)
            #
            vE=response.data_vectors['energy']
            aSol=response.samples_matrix
            
            #
            idxMinE=np.argmin(vE)
            tSol=aSol[idxMinE]
            # copy solution to variables
            self.min_configuration=tSol[0]
            self.min_energy=vE[idxMinE]
            self.energies=vE
            self.configurations=aSol
            #
            self.b=b
            #
            self.err_code=0
        elif (self.var_type.upper()=='Q'):
            '''
            ######################################################
            Ekq -> E2q -> E2s ->SOL(si)-> SOL(qi)            
            ######################################################
            '''
            print('Problem with a type-q (boolean 0/1) variable');
            varOrg,varStd,Ekq = eq_standardized(Ekx,'q')
            #
            self.var_original=varOrg
            self.var_standard=varStd
            print('Problem in symbolic standard format: ',Ekq)
            # simplifying qi**2 <- 1
            Hkq=simplify_squares(Ekq)
            print('Simplified Hkq=', Hkq)
            # Ekq-> E2q
            H2q =boole_reduce(Hkq,self.delta)
            print('H2q=', H2q)
            # ALT-1: H2q->H2s, then solve using ising SA
            # ALT-2: solve H2q using q-doman SA solver
            # ----------------------
            # choose ALT-1: H2s
            # ----------------------
            H2s=Hkq2Hks(H2q)
            #
            # solve the problem
            print('Obtaining Ising coefficients ...')
            b, hi, Jij = get_ising_coeffs(H2s)
            maxCoeff=np.max([np.max(abs(hi)), np.max(abs(Jij))])
            #
            hi=hi/maxCoeff
            Jij=Jij/maxCoeff
            #
            b=b/maxCoeff
            # put hi in the diagonal forms of Jij
            # conform with neal data format ->J
            h, J=embed_ising_coeffs(hi, Jij)
            
            '''
            -----------------------------------------------------------------------------
            4. SOLVE THE PROBLEM
            -----------------------------------------------------------------------------
            select a solver
            > dimod: ExaxtSolver
            > neal:  SimulatedAnnealingSampler
            '''
            #
            print('Solving the problem using neal  ...')
            solver=neal.SimulatedAnnealingSampler()
            response = solver.sample_ising(h, J, sweeps=self.NSWEEPS, \
                                           num_reads=self.NREADS)
            #
            vE=response.data_vectors['energy']
            aSol=response.samples_matrix
            
            #
            idxMinE=np.argmin(vE)
            tSol=aSol[idxMinE]
            # copy solution to variables
            self.min_configuration=vs2q(tSol[0])
            self.min_energy=vE[idxMinE]
            self.energies=vE
            self.configurations=vs2q(aSol)
            #
            self.b=b
            #
            self.err_code=0
        else: 
            '''
            ######################################################
            '''            
            print('Invalid problem type !!! \nShould have been either "s" or "q"');
            self.err_code=1
                   

#
def embed_ising_coeffs(hi, Jij):
    '''
    -----------------------------------------------------------------------------
    convert the problem into Ising coefficients
    -----------------------------------------------------------------------------
    '''
    #in dictionary format
    h={0:0}
    J={(0,1):1}
    
    for m in range(0,len(hi)):
        h[m]=hi[m]
        for n in range (m+1,len(hi)):
            J[m,n]=Jij[m,n]
    #
    return h, J

def genSubtitutionPairs(hoT,idxStart):
    '''
    input: hoT-a set of high order variables 
           idxStart -start index of ancillary variables
    output: list of substitution pair, [q1,q2,q3] means:  (q1*q2)<--q3
    '''
    #
    lsubP=[]
    #cp=set(qs.genSubtitutionPairs(hoT,nvTO))
    cp=set(itr.combinations(hoT,2))
    idx=idxStart
    for tz in cp:
        ttz=list(tz)
        # add ancillary variable to var pair->triple
        ttz.append(symbols('q%d'%idx))
        idx=idx+1
        lsubP.append(ttz)
    return lsubP

def H2sub(x1,x2,y,d12):
    '''
    input:  x1, x2 of x1*x2 product
            y is var result x1*x2 <-- y
            d12 compensation factor
    output:two-body polynomial compensation term
    '''
    return(d12*(3*y+x1*x2-2*x1*y-2*x2*y))

'''
There are two binary representation
    s={-1,+1} and q={0,1}
The default in Ising simulation is s-domain
------------------------------------------------------------
symbolic: q-to-s and s-t-q transform
------------------------------------------------------------
'''
def q2s(x):
    return(1/2 -x/2)

def s2q(x):
    return(1 - 2*x)

# define function vq2s
def vq2s(x):
    return(1-2*x)
# define function vs2q
def vs2q(x):
    return(1/2-x/2)

def Hks2Hkq(Hks):
    '''
    ------------------------------------------------------------
     define Hks->Hkq transform as function
    ------------------------------------------------------------
    input: Hks
    output: Hkq
    '''
    # identify free symbols
    fsS=Hks.free_symbols
    Hkq=Hks
    for tx in fsS:
        #print(ts)
        #get symbol index 
        strTx=str(tx)
        sydex=int(strTx[1:])
        syq=symbols('q%d'%sydex)
        Hkq= Hkq.subs({tx:s2q(syq)}) 
    return Hkq.expand()
#
def Hkq2Hks(Hkq):
    '''
    ------------------------------------------------------------
     define Hkq->Hks transform as function
    ------------------------------------------------------------
    input: Hkq
    output: Hks
    '''
    # identify free symbols
    fsQ=Hkq.free_symbols
    Hks=Hkq
    for tx in fsQ:
        #print(ts)
        #get symbol index 
        strTx=str(tx)
        sydex=int(strTx[1:])
        sys=symbols('s%d'%sydex)
        Hks= Hks.subs({tx:q2s(sys)}) 
    return Hks.expand()
#
""" deprecated 
def booleReduce(Hks):
    '''
    input:  k-body hamiltonian in s-domain Hks
    output: 2-body hamiltonian in s-domain H2s
    stages: Hks -> Hkq -> H2q -> H2s
    '''
    # list all involved variables
    # define higher order set >2 
    hoT=set() 
    # collection all variables in Hk
    toT=set()
    # convert Hks->Hkq
    Hkq=Hks2Hkq(Hks)
    tSet= set(Hkq.args)
    for tt in tSet:
        # get all variables in a term
        ta=tt.free_symbols # obtain var only
        toT=toT.union(ta)
        #print('ta->',ta)
        if( len(ta)>2 ):
            hoT=hoT.union(ta)
    # knowing vadiables in high order term, now construct substitution list
    # the index of ancillary variable should start after number of var in Hk
    nvTO=len(toT) # number of total variables in Hk
    nvHO=len(hoT) # number of variables involved higher order terms in Hk 
    qPair=genSubtitutionPairs(hoT,nvHO)
    # 
    delta=100
    d=delta; #2*vMax 
    '''
    # do substitution iteratively 
    '''
    H2q=Hkq
    #print(qPair)
    for tx in qPair:
        #print(tx)
        # do substitition
        #print(tx[0],'*' , tx[1], '->',tx[2] )
        H2q = H2q.subs({tx[0]*tx[1]:tx[2]} ) \
                + H2sub(tx[0], tx[1],tx[2],d)

        H2q=simplify(H2q)
    # back convert H2q->H2s
    fsQ=H2q.free_symbols
    H2s=H2q
    for tq in fsQ:
        strTx=str(tq)
        sydex=int(strTx[1:])
        sys=symbols('s%d'%sydex)
        H2s = H2s.subs( {tq:q2s(sys)})
    return expand(H2s) # hoT, toT, nvTO, nvHO #, NQ
##
"""
#
def boole_reduce(Hkq,delta):
    '''
    input:  k-body hamiltonian in q-domain Hkq
    output: 2-body hamiltonian in q-domain H2s
    stages: Hkq -> H2q
    '''
    # list all involved variables
    # define higher order set >2 
    hoT=set() 
    # collection all variables in Hk
    toT=set()
    # convert Hks->Hkq
    #Hkq=Hks2Hkq(Hks)
    tSet= set(Hkq.args)
    for tt in tSet:
        # get all variables in a term
        ta=tt.free_symbols # obtain var only
        toT=toT.union(ta)
        #print('ta->',ta)
        if( len(ta)>2 ):
            hoT=hoT.union(ta)
    # knowing vadiables in high order term, now construct substitution list
    # the index of ancillary variable should start after number of var in Hk
    nvTO=len(toT) # number of total variables in Hk
    nvHO=len(hoT) # number of variables involved higher order terms in Hk 
    qPair=genSubtitutionPairs(hoT,nvHO)
    # 
    #delta=100
    d=delta; #2*vMax 
    '''
    # do substitution iteratively 
    '''
    H2q=Hkq
    #print(qPair)
    for tx in qPair:
        #print(tx)
        # do substitition
        #print(tx[0],'*' , tx[1], '->',tx[2] )
        H2q = H2q.subs({tx[0]*tx[1]:tx[2]} ) \
                + H2sub(tx[0], tx[1],tx[2],d)

        H2q=simplify(H2q)
    #
    return expand(H2q) 
##
def eq_standardized(Hk,sqChar):
    '''
    change all input variables into a standard variables
    eg. E = x1 + x2*x4  -> E=s1 + s2*s3 
    assume EQU is already symbolic
    '''
    # get a list of all variables in the expression
    symbSet=Hk.free_symbols
    symOrg=[]
    symStd=[]
    idx=0
    for tx in symbSet:
        symOrg.append(tx)
        if (sqChar.upper()=='S'):
            tsq=symbols('s%d'%idx)
        else:
            tsq=symbols('q%d'%idx)
        symStd.append(tsq)
        # Hamiltonian with standardized variables
        Hk=Hk.subs({tx:tsq})
        '''
        symOrg[x0, x1, ..., xk]
        symStd[s0, s1, ..., sk]
        '''
        idx=idx+1
        #
    return symOrg, symStd, Hk
    

def eqString2Symbolic(EQ):
    '''
    convert string-form expression to symbolic form
    '''
    return(sympify(EQ,evaluate=False))
    
def simplifySquare(Hks):
    '''
    simplify (binary symbolic) function by assigning all
    squared variables with one: si**2 <- 1
    '''
    print('Simplifying si**2 <-1 ')
    # get all free symbols in Hks
    ss=Hks.free_symbols
    # substitute
    for ts in ss:
         Hks= Hks.subs( {ts**2:1}) 
         #print('Processing qi^2->1:',ts)
    return(simplify(Hks))
#
def simplify_squares(Hkb):
    '''
    simplify (binary symbolic) function by assigning all
    squared variables with one: bi**2 <- 1 
    where bi is a binary variable, either qi={0,1} or si{-1,+1}
    '''
    print('Simplifying bi**2 <-1 ')
    # get all free symbols in Hkb
    bb=Hkb.free_symbols
    # substitute
    for tb in bb:
         Hkb= Hkb.subs( {tb**2:1}) 
         #print('Processing qi^2->1:',ts)
    return(simplify(Hkb))


def get_ising_coeffs(H2s):
    '''
    getIsing coefficients
    input:  H2s a 2-body hamiltonian
    output: ising coeffs {hi, Jij}
    since we work in s-domain, assume the symbols are
    s0, s1, ...., s_(NQ-1)
    '''
    NQ=len(H2s.free_symbols)
    hi=np.zeros(NQ)
    Jij=np.zeros((NQ,NQ))
    dc=H2s.as_coefficients_dict()
    # list all symbols: s0, s1, ...
    ss=symbols('s0:%d'%NQ)

    # extract b
    b=dc[1]
    # extract hi
    for m in range(NQ):
        hi[m]=dc[ss[m]];
    # extract Jij
    for m in range(NQ):
        for n in range(m+1,NQ):
            #print('m=',m,'n=',n)
            Jij[m,n]=dc[ss[m]*ss[n]]
    # return the results
    return(b, hi, Jij)
#

