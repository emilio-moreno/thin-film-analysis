import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def extract_seconds_voltages(filename):
    df = pd.read_csv(filename)
    return (df.iloc[:, 3], df.iloc[:, 4])


def period_calculation(seconds, voltages, bound, match_lengths = False):
    '''
    Calculates period of motor from voltage and the time of given period.
    bound: bound voltage for event (see below)
    match_lengths: makes times-of-period array match length of periods array.
    '''
    # In order to calculate the period we need to find an event that only
    # happens once per cycle and at regular intervals.
    # We'll consider a bound voltage value. We suppose that there's only
    # one data point per cycle that satisfies being below this bound voltage
    # and whose next data point is above this bound voltage.
    # This is our "event" which in real life may correspond to
    # the laser inciding on the black tape to inciding on the reflecting surface.
    # Period calculation will be done considering this event so
    # bound (voltage) must be selected so as to .only be satisfied once per cycle.

    # We pick a list of seconds whose voltages satisfy the event.
    # As the event is satisfied once per cycle, we'll be able to determine   
    # the period by finding the diferences between these times.
    event_seconds = np.array([])
    for s, v, v_next in zip(seconds, voltages, voltages[1:]):
        if v <= bound and v_next > bound:
            event_seconds = np.append(event_seconds, s)

    # We take the average of the time differences between four pairs of points centered at our current time.
    #periods = np.array([np.mean([event_seconds[i - 1] - event_seconds[i - 2], event_seconds[i] - event_seconds[i - 1], event_seconds[i + 1] - event_seconds[i], event_seconds[i + 2] - event_seconds[i + 1]]) for i in range(2, len(event_seconds) - 2)])
    periods = np.array([event_seconds[i] - event_seconds[i - 1] for i in range(1, len(event_seconds))])

    if match_lengths:
        return event_seconds[2:-2], periods
    return event_seconds, periods


def main():
    #Get data
    RPM = []
    std = []
    directory = "./11-09-24 PDMS/RPM"
    listdir = os.listdir(directory)
    listdir = sorted(listdir)
    os.chdir(directory)
    acceleration_tek = ['02', '05', '08']

    filenames = []
    for filename in listdir:
        if filename[-6:-4] in acceleration_tek:
            continue
        filenames.append(filename)

        s, v = extract_seconds_voltages(filename)
        t , T = period_calculation(s, v, 0.1)
        rpm =  60 / T
        RPM.append(np.mean(rpm))
        std.append(np.std(rpm)/np.sqrt(len(rpm)))
        
        # graph(t, T, filename)

    df = pd.DataFrame({'filename': filenames, 'RPM': RPM, 'std': std})
    df.to_csv('../11-09-24_RPM.CSV')
    print(df)


def graph(t, T, title):
    fig, ax = plt.subplots()
    ax.plot(t[:-1], T)

    # Format
    ax.set(title = title, xlabel = "Wavelength (nm)", ylabel = "Trans (%)")
    ax.grid(color = '#999', linestyle = '--')

    figManager = plt.get_current_fig_manager()
    figManager.full_screen_toggle()
    plt.show()



if __name__ == "__main__":
    main()
