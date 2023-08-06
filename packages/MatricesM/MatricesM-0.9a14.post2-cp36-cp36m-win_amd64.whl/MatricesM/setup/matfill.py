def setMatrix(mat,d=None,r=None,lis=[],direc=r"",fill="uniform"):
    """
    Set the matrix based on the arguments given
    """
    from random import random,uniform,triangular,gauss,seed
    from MatricesM.C_funcs.randgen import getuni,getfill,igetuni,igetrand
    from MatricesM.C_funcs.zerone import pyfill
    from MatricesM.C_funcs.linalg import Ctranspose
    # =============================================================================
    # Argument check
    if lis is None:
        lis = []
    if len(direc)==0 and len(lis)==0:
        if fill == None:
            fill = "uniform"
        if not fill in ["uniform","gauss","triangular"]:
            while True:
                try:
                    fill=complex(fill)
                    if fill.imag==0:
                        fill = fill.real
                except:
                    raise ValueError("fill should be one of ['uniform','triangular','gauss'] or an integer | a float | a complex number")
                else:
                    break
    mat._setDim(d)
    #Set new range    
    if r==None:
        r=mat.initRange
    else:
        mat._Matrix_initRange=r
        
    # =============================================================================
    #Save the seed for reproduction
    if mat.seed==None and mat.fill in ["random","uniform","gauss","triangular"] and len(lis)==0 and len(direc)==0:
        randseed=random()
        seed(randseed)
        mat._Matrix_seed=randseed
        
    elif mat.fill in ["random","uniform","gauss","triangular"] and len(lis)==0 and len(direc)==0:
        seed(mat.seed)
    else:
        mat._Matrix_seed=None
        
    # =============================================================================
    #Set the new matrix
    if isinstance(lis,str):
        mat._matrix=mat._listify(lis)
        if mat.dim == [0,0]:
            mat._Matrix__dim=mat._declareDim()
    elif len(direc)>0:
        lis=mat._Matrix__fromFile(direc)
        if not lis==None:
            mat._matrix=mat._listify(lis)
        else:
            return None
        if mat.dim == [0,0]:
            mat._Matrix__dim=mat._declareDim()          
    else:
        if len(lis)>0:
            if isinstance(lis[0],list):                        
                mat._matrix = [a[:] for a in lis[:]]
                if mat.dim == [0,0]:
                    mat._Matrix__dim=mat._declareDim()
            else:
                try:
                    assert mat.dim[0]*mat.dim[1] == len(lis)
                except Exception as err:
                    print(err)
                else:
                    mat._matrix=[]
                    for j in range(0,len(lis),mat.dim[1]):
                            mat._matrix.append(lis[j:j+mat.dim[1]])
            
        # =============================================================================
        #Same range for all columns
        elif len(lis)==0 and (isinstance(r,list) or isinstance(r,tuple)):
            
            if mat.fill in ["uniform"]:
                m,n=max(r),min(r)
                if mat._cMat:
                    mat._matrix=[[complex(uniform(n,m),uniform(n,m)) for a in range(d[1])] for b in range(d[0])]
                
                elif mat._fMat:
                    if r==[0,1]:
                        mat._matrix=pyfill(d[0],d[1])
                    else:
                        mat._matrix=getuni(d[0],d[1],n,m)
                
                else:
                    if r==[0,1]:
                        mat._matrix=igetrand(d[0],d[1])
                    else:
                        m+=1
                        mat._matrix=igetuni(d[0],d[1],n,m)
                        
            elif mat.fill in ["gauss"]:
                m,s=r[0],r[1]
                if mat._cMat:
                    mat._matrix=[[complex(gauss(m,s),gauss(m,s)) for a in range(d[1])] for b in range(d[0])]
                
                elif mat._fMat:
                        mat._matrix=[[gauss(m,s) for a in range(d[1])] for b in range(d[0])]
                
                else:
                    mat._matrix=[[round(gauss(m,s)) for a in range(d[1])] for b in range(d[0])]
                    
            elif mat.fill in ["triangular"]:
                n,m,o = r[0],r[1],r[2]
                if mat._cMat:
                    mat._matrix=[[complex(triangular(n,m,o),triangular(n,m,o)) for a in range(d[1])] for b in range(d[0])]
                
                elif mat._fMat:
                        mat._matrix=[[triangular(n,m,o) for a in range(d[1])] for b in range(d[0])]
                else:
                    mat._matrix=[[round(triangular(n,m,o)) for a in range(d[1])] for b in range(d[0])]   
                    
            else:
                mat._matrix=getfill(d[0],d[1],fill)
        # =============================================================================               
        #Different ranges over individual columns
        elif len(lis)==0 and isinstance(r,dict):
            try:
                assert len([i for i in r.keys()])==mat.dim[1]
                vs=[len(i) for i in r.values()]
                assert vs.count(vs[0])==len(vs)
                feats=[i for i in r.keys()]
                mat.features=feats
  
            except Exception as err:
                print(err)
            else:
                lis=list(r.values())
                if mat.fill in ["uniform"]:                    
                    if mat._cMat:
                        temp=[[complex(uniform(min(lis[i]),max(lis[i])),uniform(min(lis[i]),max(lis[i]))) for _ in range(d[0])] for i in range(d[1])]
                    
                    elif mat._fMat:
                        temp=[[uniform(min(lis[i]),max(lis[i])) for _ in range(d[0])] for i in range(d[1])]                        
                    
                    else:
                        temp=[[round(uniform(min(lis[i]),max(lis[i])+1))//1 for _ in range(d[0])] for i in range(d[1])]
                
                elif mat.fill in ["gauss"]:                    
                    if mat._cMat:
                        temp=[[complex(gauss(lis[i][0],lis[i][1]),uniform(min(lis[i]),max(lis[i]))) for _ in range(d[0])] for i in range(d[1])]
                    
                    elif mat._fMat:
                        temp=[[gauss(lis[i][0],lis[i][1]) for _ in range(d[0])] for i in range(d[1])]                        
                    
                    else:
                        temp=[[round(gauss(lis[i][0],lis[i][1]+1))//1 for _ in range(d[0])] for i in range(d[1])]
                        
                elif mat.fill in ["triangular"]:                    
                    if mat._cMat:
                        temp=[[complex(triangular(lis[i][0],lis[i][1],lis[i][2]),triangular(lis[i][0],lis[i][1],lis[i][2])) for _ in range(d[0])] for i in range(d[1])]
                        
                    elif mat._fMat:
                        
                        temp=[[triangular(lis[i][0],lis[i][1],lis[i][2]) for _ in range(d[0])] for i in range(d[1])]                                                
                    else:
                        temp=[[round(triangular(lis[i][0],lis[i][1]+1,lis[i][2]))//1 for _ in range(d[0])] for i in range(d[1])]
                
                else:
                    mat._matrix=[[lis[b] for a in range(d[1])] for b in range(d[0])]
                
                mat._matrix=Ctranspose(d[1],d[0],temp)
        else:
            return None
