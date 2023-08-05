from __future__ import print_function, division
from wotan import flatten, t14
import numpy
from astropy.io import fits


def load_file(filename):
    """Loads a TESS *spoc* FITS file and returns TIME, PDCSAP_FLUX"""
    hdu = fits.open(filename)
    time = hdu[1].data['TIME']
    flux = hdu[1].data['PDCSAP_FLUX']
    flux[flux == 0] = numpy.nan
    return time, flux


def main():
    print("Starting tests for wotan...")

    numpy.testing.assert_almost_equal(
        t14(R_s=1, M_s=1, P=365),
        0.6489947464173134)

    numpy.testing.assert_almost_equal(
        t14(R_s=1, M_s=1, P=365, small_planet=True),
        0.5403625370706341)
    print("Transit duration correct.")

    numpy.random.seed(seed=0)  # reproducibility

    # TESS test
    print('Loading TESS data from archive.stsci.edu...')
    filename = "https://archive.stsci.edu/hlsps/tess-data-alerts/" \
    "hlsp_tess-data-alerts_tess_phot_00062483237-s01_tess_v1_lc.fits"

    #filename = "hlsp_tess-data-alerts_tess_phot_00062483237-s01_tess_v1_lc.fits"
    #filename = 'P:/P/Dok/tess_alarm/hlsp_tess-data-alerts_tess_phot_00077031414-s02_tess_v1_lc.fits'
    #filename = 'tess2018206045859-s0001-0000000201248411-111-s_llc.fits'
    time, flux = load_file(filename)

    window_length = 0.5

    print("Detrending 1 (biweight)...")
    flatten_lc, trend_lc = flatten(
        time,
        flux,
        window_length,
        edge_cutoff=1,
        break_tolerance=0.1,
        return_trend=True,
        cval=5.0)

    numpy.testing.assert_equal(len(trend_lc), 20076)
    numpy.testing.assert_almost_equal(numpy.nanmax(trend_lc), 28754.985299070882)
    numpy.testing.assert_almost_equal(numpy.nanmin(trend_lc), 28615.108124724477)
    numpy.testing.assert_almost_equal(trend_lc[500], 28671.686308143515)

    numpy.testing.assert_equal(len(flatten_lc), 20076)
    numpy.testing.assert_almost_equal(numpy.nanmax(flatten_lc), 1.0034653549250616)
    numpy.testing.assert_almost_equal(numpy.nanmin(flatten_lc), 0.996726610702177)
    numpy.testing.assert_almost_equal(flatten_lc[500], 1.000577429565131)

    print("Detrending 2 (andrewsinewave)...")
    flatten_lc, trend_lc = flatten(time, flux, window_length, method='andrewsinewave', return_trend=True)
    numpy.testing.assert_almost_equal(numpy.nansum(flatten_lc), 18119.15471987987, decimal=2)

    print("Detrending 3 (welsch)...")
    flatten_lc, trend_lc = flatten(time, flux, window_length, method='welsch', return_trend=True)
    numpy.testing.assert_almost_equal(numpy.nansum(flatten_lc), 18119.16764691235, decimal=2)

    print("Detrending 4 (hodges)...")
    flatten_lc, trend_lc = flatten(time[:1000], flux[:1000], window_length, method='hodges', return_trend=True)
    numpy.testing.assert_almost_equal(numpy.nansum(flatten_lc), 994.0110525909206, decimal=2)

    print("Detrending 5 (median)...")
    flatten_lc, trend_lc = flatten(time, flux, window_length, method='median', return_trend=True)
    numpy.testing.assert_almost_equal(numpy.nansum(flatten_lc), 18119.122065014355, decimal=2)

    print("Detrending 6 (mean)...")
    flatten_lc, trend_lc = flatten(time, flux, window_length, method='mean', return_trend=True)
    numpy.testing.assert_almost_equal(numpy.nansum(flatten_lc), 18119.032473037714, decimal=2)

    print("Detrending 7 (trim_mean)...")
    flatten_lc, trend_lc = flatten(time, flux, window_length, method='trim_mean', return_trend=True)
    numpy.testing.assert_almost_equal(numpy.nansum(flatten_lc), 18119.095164910334, decimal=2)

    print("Detrending 8 (supersmoother)...")
    flatten_lc, trend_lc = flatten(time, flux, window_length, method='supersmoother', return_trend=True)
    numpy.testing.assert_almost_equal(numpy.nansum(flatten_lc), 18123.00632204841, decimal=2)

    print("Detrending 9 (hspline)...")
    flatten_lc, trend_lc = flatten(time, flux, window_length, method='hspline', return_trend=True)
    numpy.testing.assert_almost_equal(numpy.nansum(flatten_lc), 18123.07625225313, decimal=2)

    print("Detrending 10 (cofiam)...")
    flatten_lc, trend_lc = flatten(time[:2000], flux[:2000], window_length, method='cofiam', return_trend=True)
    numpy.testing.assert_almost_equal(numpy.nansum(flatten_lc), 1948.9999999987976, decimal=2)

    print("Detrending 11 (savgol)...")
    flatten_lc, trend_lc = flatten(time, flux, window_length=301, method='savgol', return_trend=True)
    numpy.testing.assert_almost_equal(numpy.nansum(flatten_lc), 18123.003465539354, decimal=2)

    print("Detrending 12 (medfilt)...")
    flatten_lc, trend_lc = flatten(time, flux, window_length=301, method='medfilt', return_trend=True)
    numpy.testing.assert_almost_equal(numpy.nansum(flatten_lc), 18123.22609806557, decimal=2)

    print("Detrending 12 (gp squared_exp)...")
    flatten_lc, trend_lc1 = flatten(
        time[:2000],
        flux[:2000],
        method='gp',
        kernel='squared_exp',
        kernel_size=10,
        return_trend=True)
    numpy.testing.assert_almost_equal(numpy.nansum(flatten_lc), 1948.99958552324, decimal=2)

    print("Detrending 13 (gp matern)...")
    flatten_lc, trend_lc2 = flatten(
        time[:2000],
        flux[:2000],
        method='gp',
        kernel='matern',
        kernel_size=10,
        return_trend=True)
    numpy.testing.assert_almost_equal(numpy.nansum(flatten_lc), 1949.0001583058202, decimal=2)

    print("Detrending 14 (gp periodic)...")
    flatten_lc, trend_lc2 = flatten(
        time[:2000],
        flux[:2000],
        method='gp',
        kernel='periodic',
        kernel_size=1,
        kernel_period=10,
        return_trend=True)
    numpy.testing.assert_almost_equal(numpy.nansum(flatten_lc), 1948.9999708985608, decimal=2)

    time_synth = numpy.linspace(0, 30, 200)
    flux_synth = numpy.sin(time_synth) + numpy.random.normal(0, 0.1, 200)
    flux_synth = 1 + flux_synth / 100
    time_synth *= 1.5
    print("Detrending 15 (gp periodic_auto)...")
    flatten_lc, trend_lc2 = flatten(
        time_synth,
        flux_synth,
        method='gp',
        kernel='periodic_auto',
        kernel_size=1,
        return_trend=True)
    numpy.testing.assert_almost_equal(numpy.nansum(flatten_lc), 200, decimal=1)
    
    print("Detrending 15 (untrendy)...")
    flatten_lc, trend_lc2 = flatten(
        time,
        flux,
        method='untrendy',
        window_length=1,
        return_trend=True)
    numpy.testing.assert_almost_equal(numpy.nansum(flatten_lc), 18122.997281790234, decimal=2)


    print("Detrending 16 (huber)...")
    flatten_lc, trend_lc = flatten(
        time[:1000],
        flux[:1000],
        method='huber',
        window_length=0.5,
        edge_cutoff=0,
        break_tolerance=0.4,
        return_trend=True)
    numpy.testing.assert_almost_equal(numpy.nansum(flatten_lc), 994.01102, decimal=2)

    print("Detrending 17 (winsorize)...")
    flatten_lc, trend_lc2 = flatten(
        time,
        flux,
        method='winsorize',
        window_length=0.5,
        edge_cutoff=0,
        break_tolerance=0.4,
        proportiontocut=0.1,
        return_trend=True)
    numpy.testing.assert_almost_equal(numpy.nansum(flatten_lc), 18119.064587196448, decimal=2)

    """
    import matplotlib.pyplot as plt
    plt.scatter(time, flux, s=1, color='black')
    #plt.plot(time[:2000], trend_lc1[:2000], color='red')
    plt.plot(time, trend_lc, color='red', linewidth=2)
    plt.plot(time, trend_lc2, color='blue', linewidth=2)
    plt.show()
    plt.close()
    plt.scatter(time, flatten_lc, s=1, color='black')
    plt.show()
    """

    print('All tests completed.')


if __name__ == '__main__':
    main()