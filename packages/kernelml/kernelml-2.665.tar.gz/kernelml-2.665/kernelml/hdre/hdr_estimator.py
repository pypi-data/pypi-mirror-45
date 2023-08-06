import time
import numpy as np
import numpy
import kernelml
from .hdr_helpers_bycython import *

class ArgumentError(Exception):
    pass

### HDRE
class HDRE():

    def __init__(self,number_of_clusters, bins_per_dimension=13, number_of_random_simulations=500, number_of_realizations=20, smoothing_parameter=2.0):

        self.num_clusters = number_of_clusters
        self.simulations = number_of_random_simulations
        self.realizations = number_of_realizations
        self.smoothing_parameter = smoothing_parameter
        self.bins_per_dim = bins_per_dimension
        self.kmldata = None
        self.norm = 1
    
        if (self.bins_per_dim/2 == self.bins_per_dim//2+1):
            raise ArgumentError("The number of bins per dimensions must be an odd integer")

    def optimize(self,X,y=None,agg_func='count',dview=None):

        def loss_func(X,y,w,args):
            np=numpy
            return hdre_loss(X,y,w,args)
        
        
        maxs = np.max(X,axis=0)
        mins = np.min(X,axis=0)
        widths = (maxs-mins)/(self.bins_per_dim)
        maxs+=3*widths
        mins-=3*widths
        widths = (maxs-mins)/(self.bins_per_dim)
        
        dim_bins = [np.linspace(m0,m1,self.bins_per_dim) for m0,m1 in zip(mins,maxs)]
        dim_combos = [(i,j) for i in range(X.shape[1]) for j in range(X.shape[1]) if j>i]
        
        half = (self.bins_per_dim)//2
        mesh = np.meshgrid(*[np.arange(-(half),half+1,1) for _ in range(2)])
        mesh = [d**2 for d in mesh]
        sigma = self.smoothing_parameter
        kernel = np.exp(-sum(mesh)/(2*sigma**2))/np.sqrt(2*np.pi*sigma**2)
        kernel = kernel/np.sum(kernel)
        fftkernel = np.fft.fftn(kernel)

        self.dim_combos = dim_combos
        combo_len = len(dim_combos)
        pdf_combos = np.zeros((combo_len,self.bins_per_dim,self.bins_per_dim))
        bin_combos = np.zeros((combo_len,self.bins_per_dim,2))
        count=0
        for i,j in dim_combos:
            _X_ = X[:,[i,j]]
            bins3 = [dim_bins[i],dim_bins[j]]
#             bins3 = [np.concatenate([[-np.inf],_bins_,[np.inf]]) for _bins_ in bins3]
            bin_combos[count] = np.column_stack(bins3)
            data,_ = hdre_histogram(_X_,y,agg_func=agg_func,bins=bins3)
            data=data/np.sum(data)
            pdf_combos[count] = np.fft.fftshift(np.real(np.fft.ifftn(np.fft.fftn(data)*fftkernel)))
            count+=1


        cycles = 100

        #The number of total simulations per realization = number of cycles * numer of simulations

        self.num_dim = X.shape[1]
        
        zcore = 2.0
        volume = 10 + self.num_dim+self.num_clusters
        volatility = 1
        zscore = 1

        self.num_rot = self.num_clusters*combo_len
        param_to_dim = np.arange(0,self.num_dim*self.num_clusters)%self.num_dim
        
        args = [dim_combos,pdf_combos,bin_combos,fftkernel,mins,maxs,
                param_to_dim,self.num_dim,self.num_clusters*combo_len,widths]

        if self.kmldata is None:
            self.kml = kernelml.KernelML(
                 prior_sampler_fcn=hdre_prior_sampler,
                 posterior_sampler_fcn=None,
                 intermediate_sampler_fcn=None,
                 mini_batch_sampler_fcn=None,
                 parameter_transform_fcn=hdre_parameter_transform,
                 batch_size=None)

            if dview is not None:
                 self.kml.use_ipyparallel(dview)

        self.kml.optimize(X[:1],np.array([[]]),loss_function=loss_func,
                                        convergence_z_score=3.0,
                                        min_loss_per_change=0.0,
                                        number_of_parameters=self.num_clusters*self.num_dim+self.num_dim+self.num_clusters*combo_len,
                                        args=args,
                                        number_of_realizations=self.realizations,
                                        number_of_random_simulations=self.simulations,
                                        update_volume=volume,
                                        update_volatility=volatility,
                                        number_of_cycles=cycles,
                                        print_feedback=True)

        self.kmldata = self.kml.kmldata
        
        self.kml.load_kmldata(self.kmldata)
    


    @property
    def variance_(self):
        w = self.kmldata.best_weight_vector.flatten()
        return np.abs(w[:self.num_dim]).reshape(self.num_dim,1)
    
    @property
    def rotations_(self):
        w = self.kmldata.best_weight_vector.flatten()
        w = w[self.num_dim:self.num_dim+self.num_rot]
        return w
    
    @property
    def centroids_(self):
        w = self.kmldata.best_weight_vector.flatten()
        w = w[self.num_dim+self.num_rot:]
        return w.reshape((w.size//self.num_dim,self.num_dim))
    
    def get_assignments(self,X,pad=1):
        var = self.variance_
        rot = self.rotations_
        mean = self.centroids_
        mask = np.zeros((X.shape[0],self.num_clusters),dtype=np.bool)
        count=0
        for i,j in self.dim_combos:
            for k in range(self.num_clusters):
                S = np.array([[var[i],0],[0,var[j]]])
                theta = rot[count]
                R = np.array([[np.cos(theta),-np.sin(theta)],[np.sin(theta),np.cos(theta)]])

                T = (S*pad).dot(R)

                points = np.array([[-1.,1.],[1.,1.],[1.,-1.],[-1.,-1.],[-1.,1.]])
                points = points.dot(T)
                points[:,0] = points[:,0]+mean[k,i]
                points[:,1] = points[:,1]+mean[k,j]
                
                P = points.copy()

                angles = np.zeros((y.shape[0]))
                for b in range(4):
                    a = X[:,[i,j]]-P[b]
                    v = X[:,[i,j]]-P[b+1]
                    d = v[:,0]*a[:,1]-v[:,1]*a[:,0]
                    angles+=(d>0)

                mask[:,k] = mask[:,k]|((angles!=4)&(angles!=0))

                count+=1
        return ~mask
