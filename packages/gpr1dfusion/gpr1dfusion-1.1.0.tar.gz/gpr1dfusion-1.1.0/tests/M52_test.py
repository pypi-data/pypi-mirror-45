#!/usr/bin/env python

import os
import sys
import re
import copy
import numpy as np

import gpr1dfusion      # Required import, only works after using 'pip install'


def run_test():
    """
    A demonstration script for the classes within the gpr1dfusion module.

    Due to the iterative nature of the optimization method and the
    random nature of the kernel restart function, the results may
    not be exactly the same for consecutive runs of this demo
    script. However, all fits should fall within the fit error
    ranges of each other, unless the optimization algorithm has
    not converged.
    """

    ### Some basic setup

    plot_save_directory = './gpr1dfusion_test_plots/'
    if not plot_save_directory.endswith('/'):
        plot_save_directory = plot_save_directory + '/'
    if not os.path.isdir(plot_save_directory):
        os.makedirs(plot_save_directory)


    ### Generating sample data

    # Make basic function data
    x_spread = 0.01
    y_spread = 0.25
    intercept = 3.0
    slope1 = 1.0
    x_values = np.linspace(0.0,1.0,21)
    y_values = slope1 * x_values + intercept
    boundary1 = 0.3
    slope2 = 16.0
    boundary1_filter = (x_values >= boundary1)
    y_values[boundary1_filter] = y_values[boundary1_filter] - slope2 * (x_values[boundary1_filter] - boundary1)
    boundary2 = 0.7
    boundary2_filter = (x_values >= boundary2)
    y_values[boundary2_filter] = y_values[boundary2_filter] + (slope2 + slope1) * (x_values[boundary2_filter] - boundary2)

    # Add random error to generated data points
    raw_x_values = x_values + x_spread * np.random.randn(x_values.size)
    raw_y_values = y_values + y_spread * np.random.randn(y_values.size)
    raw_x_errors = np.full(raw_x_values.shape,x_spread)
    raw_y_errors = np.full(raw_y_values.shape,y_spread)
    raw_intercept = raw_y_values[0]



    ### Fitting

    fit_x_values = np.linspace(0.0,1.0,100)

    # Define a kernel to fit the data itself
    #     Rational quadratic kernel is usually robust enough for general fitting
    gpr_object = gpr1dfusion.Matern52FGPR1D(raw_x_values,raw_y_values,raw_y_errors,amplitude=1.0e0,length_scale=1.0e0,nrestarts=5)

    #     Perform the fit with kernel restarts, returns fit results
    (fit_y_values,fit_y_errors,fit_dydx_values,fit_dydx_errors) = gpr_object(fit_x_values)

    #     Grab optimized kernel settings - easy way to minimize data storage requirements for fit reproduction
    (gp_kernel_name,gp_kernel_hyppars,gp_fit_regpar) = gpr_object.get_gp_kernel_details()

    #     Grab the log-marginal-likelihood of fit
    fit_lml = gpr_object.get_gp_lml()



    ### Sampling distribution

    num_samples = 10
    sample_array = None
    dsample_array = None

    # Samples the fit distribution
    for ii in np.arange(0,num_samples):
        sample = gpr_object.sample(fit_x_values,derivative=False)
        sample_array = np.vstack((sample_array,sample)) if sample_array is not None else copy.deepcopy(sample)

    # Samples the derivative distribution
    for ii in np.arange(0,num_samples):
        dsample = gpr_object.sample(fit_x_values,derivative=True)
        dsample_array = np.vstack((dsample_array,dsample)) if dsample_array is not None else copy.deepcopy(dsample)

    # Computing statistics of sampled profiles
    sample_mean = np.nanmean(sample_array,axis=0)
    dsample_mean = np.nanmean(dsample_array,axis=0)
    sample_std = np.nanstd(sample_array,axis=0)
    dsample_std = np.nanstd(dsample_array,axis=0)



    ### Printing

    gp_str = "\n--- GPR Fit ---\n\n"
    gp_str = gp_str + "Kernel name: %30s\n" % (gp_kernel_name)
    gp_str = gp_str + "Regularization parameter: %17.4f\n" % (gp_fit_regpar)
    gp_str = gp_str + "Optimized kernel hyperparameters:\n"
    for hh in np.arange(0,gp_kernel_hyppars.size):
        gp_str = gp_str + "%15.6e" % (gp_kernel_hyppars[hh])
    gp_str = gp_str + "\n\n"
    gp_str = gp_str + "Log-marginal-likelihood: %18.6f\n" % (fit_lml)

    print(gp_str)



    ### Plotting

    plt = None
    try:
        import matplotlib.pyplot as plt
    except:
        plt = None

    if plt is not None:

        plot_sigma = 1.0

        # Raw data with GPR fit and error, only accounting for y-errors
        plot_raw_y_errors = plot_sigma * raw_y_errors
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.errorbar(raw_x_values,raw_y_values,yerr=plot_raw_y_errors,ls='',marker='.',color='g')
        ax.plot(fit_x_values,fit_y_values,color='r')
        plot_fit_y_lower = fit_y_values - plot_sigma * fit_y_errors
        plot_fit_y_upper = fit_y_values + plot_sigma * fit_y_errors
        ax.fill_between(fit_x_values,plot_fit_y_lower,plot_fit_y_upper,facecolor='r',edgecolor='None',alpha=0.2)
        for ii in np.arange(0,num_samples):
            ax.plot(fit_x_values,sample_array[ii,:],color='k',alpha=0.5)
        ax.set_xlim(0.0,1.0)
        fig.savefig(plot_save_directory+'m52_test.png')
        plt.close(fig)

        # Derivative of GPR fit and error, only accounting for y-errors
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(fit_x_values,fit_dydx_values,color='r')
        plot_fit_dydx_lower = fit_dydx_values - plot_sigma * fit_dydx_errors
        plot_fit_dydx_upper = fit_dydx_values + plot_sigma * fit_dydx_errors
        ax.fill_between(fit_x_values,plot_fit_dydx_lower,plot_fit_dydx_upper,facecolor='r',edgecolor='None',alpha=0.2)
        for ii in np.arange(0,num_samples):
            ax.plot(fit_x_values,dsample_array[ii,:],color='k',alpha=0.5)
        ax.set_xlim(0.0,1.0)
        fig.savefig(plot_save_directory+'m52_dtest.png')
        plt.close(fig)

        print("Results of M52 kernel test plotted in directory %s\n" % (plot_save_directory))

    else:

        print("   Module matplotlib not found. Skipping plotting of demonstration results.\n")

    print("Demonstration script successfully completed!\n")


def main():

    run_test()


if __name__ == "__main__":

    main()
