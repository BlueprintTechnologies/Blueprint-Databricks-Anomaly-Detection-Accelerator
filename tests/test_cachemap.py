#!/usr/bin/env python
"""
Created on Monday, March 21, 2022 at 14:33:41 by 'Wesley Cobb <wesley@bpcs.com>'
Copyright (C) 2022, by Blueprint Technologies. All Rights Reserved.
 
Last edited: <2022-03-31 09:13:06 wcobb>
 
"""
#
# standard imports
#
import os
import math
import pandas as pd
import numpy as np
from scipy.stats import mode
import matplotlib.pyplot as plt
import geopandas as gpd
from tqdm import tqdm
import dill

import threat
from threat.core import loader, places
from threat.core import public_address
from threat.core import Cache

def traffic_proto_ranking(traffic_proto):    
    #
    # define them...
    #
    utp = np.unique(traffic_proto)
    #
    # initialize a dictionary...
    #
    utp_freqs = {}
    for key in utp:
        if (key not in utp_freqs.keys()):
            utp_freqs[key] = 0
    #
    # count them...
    #
    for tp in traffic_proto:
        utp_freqs[tp] += 1
    #
    # rank them...
    #
    ranking = []
    for key in utp_freqs.keys():
        ranking.append((utp_freqs[key], key))
    sranking = sorted(ranking, reverse = True)
    total = np.sum([s for (s,p) in sranking])
    nsranking = [(100*s/total,p) for (s,p) in sranking]
    return nsranking

def display_metrics(population:{}, min_count:int = 1, num_bins = 20, show_histograms:bool = False, show_table:bool = True):
    """
    """
    if (show_table):
        print("ProtocolName        median(F)    median(D)     median(V)     median(A)     median(R)     median(P)")
        print("----------------- ------------ ------------  ------------  ------------  ------------  ------------")
    
    for proto in population.keys():
        if ((show_table) and (population[proto]["metrics"]["flowrate"]["count"] >= min_count)):
            print("%17s %12d %12d %12d %12d %12d %12d" % 
                  ((proto+"                 ")[0:17],
                   population[proto]["metrics"]["flowrate"]["median"],
                   population[proto]["metrics"]["duration"]["median"],
                   population[proto]["metrics"]["volume"]["median"],
                   population[proto]["metrics"]["avpktsz"]["median"],
                   population[proto]["metrics"]["dnuprat"]["median"],
                   population[proto]["metrics"]["pktlenvar"]["median"],
                  )
            )
        #
        # we're going to make 1 figure for each quantity for which we have at least
        # 1000 observations...
        #
        main_title = 24
        pane_title = 18
        pane_text = 16
        if (population[proto]["metrics"]["flowrate"]["count"] >= min_count):
            #
            # create the overall image and add the title...
            #
            fig, ax = plt.subplots(3, 3, figsize=(30, 30))
            plt.suptitle(f"Key Histograms for {proto}", fontsize = main_title)
            #
            # 1st col, 1st row...
            #
            ax[0][0].set_title("Flow Rate (bytes/sec)", fontsize = pane_title)
            ax[0][0].set_xlabel("Bin", fontsize = pane_text)
            ax[0][0].set_ylabel("log10(Counts)", fontsize = pane_text)
            ax[0][0].set_yscale('log')
            ax[0][0].hist(population[proto]["metrics"]["flowrate"]["data"], color = "blue",  bins = num_bins)
            #
            # 1st col, 2nd row...
            #
            ax[0][1].set_title("Duration (secs)", fontsize = pane_title)
            ax[0][1].set_yscale('log')
            ax[0][1].hist(population[proto]["metrics"]["duration"]["data"], color = "red", bins = num_bins)
            ax[0][1].set_xlabel("Bin", fontsize = pane_text)
            ax[0][1].set_ylabel("log10(Counts)", fontsize = pane_text)
            #
            # 1st col, 3rd row...
            #
            ax[0][2].set_title("Volume (bytes)", fontsize = pane_title)
            ax[0][2].set_yscale('log')
            ax[0][2].hist(population[proto]["metrics"]["volume"]["data"], color = "green", bins = num_bins)
            ax[0][2].set_xlabel("Bin", fontsize = pane_text)
            ax[0][2].set_ylabel("log10(Counts)", fontsize = pane_text)
            #
            # 2nd col, 1st row...
            #
            ax[1][0].set_title("Average Packet Size (bytes)", fontsize = pane_title)
            ax[1][0].set_xlabel("Bin", fontsize = pane_text)
            ax[1][0].set_ylabel("log10(Counts)", fontsize = pane_text)
            ax[1][0].set_yscale('log')
            ax[1][0].hist(population[proto]["metrics"]["avpktsz"]["data"], color = "magenta",  bins = num_bins)
            #
            # 2nd col, 2nd row...
            #
            ax[1][1].set_title("Down Up Ratio", fontsize = pane_title)
            ax[1][1].set_yscale('log')
            ax[1][1].hist(population[proto]["metrics"]["dnuprat"]["data"], color = "cyan", bins = num_bins)
            ax[1][1].set_xlabel("Bin", fontsize = pane_text)
            ax[1][1].set_ylabel("log10(Counts)", fontsize = pane_text)
            #
            # 2nd col, 3rd row...
            #
            ax[1][2].set_title("Packet Length Variance", fontsize = pane_title)
            ax[1][2].set_yscale('log')
            ax[1][2].hist(population[proto]["metrics"]["pktlenvar"]["data"], color = "brown", bins = num_bins)
            ax[1][2].set_xlabel("Bin", fontsize = pane_text)
            ax[1][2].set_ylabel("log10(Counts)", fontsize = pane_text)
            #
            # 3rd col, 1st row...
            #
            ax[2][0].set_title("Forward Packet Length Mean (bytes)", fontsize = pane_title)
            ax[2][0].set_xlabel("Bin", fontsize = pane_text)
            ax[2][0].set_ylabel("log10(Counts)", fontsize = pane_text)
            ax[2][0].set_yscale('log')
            ax[2][0].hist(population[proto]["metrics"]["fwdpktlen"]["data"], color = "orange",  bins = num_bins)
            #
            # 3rd col, 2nd row...
            #
            ax[2][1].set_title("Backward Packet Length Mean (bytes)", fontsize = pane_title)
            ax[2][1].set_yscale('log')
            ax[2][1].hist(population[proto]["metrics"]["bwdpktlen"]["data"], color = "lightgreen", bins = num_bins)
            ax[2][1].set_xlabel("Bin", fontsize = pane_text)
            ax[2][1].set_ylabel("log10(Counts)", fontsize = pane_text)
            #
            # 3rd col, 3rd row...
            #
            ax[2][2].set_title("Active Mean", fontsize = pane_title)
            ax[2][2].set_yscale('log')
            ax[2][2].hist(population[proto]["metrics"]["actmean"]["data"], color = "indigo", bins = num_bins)
            ax[2][2].set_xlabel("Bin", fontsize = pane_text)
            ax[2][2].set_ylabel("log10(Counts)", fontsize = pane_text)
            #
            # save/display or whatever...
            #
            plt.savefig(os.path.join(places("images"), f"{proto}_histogram.png"))
            if (show_histograms):
                plt.show()
            else:
                plt.close()
    return None

def display_world(slatlon, dlatlon, traffic_color, dur, bps, show_world = False):
    """
    """
    fig, ax = plt.subplots(2, 1, figsize = (24, 24))
    worldmap = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
    worldmap.plot(color = "lightgrey", ax = ax[0])
    #
    # the inbound traffic map...
    #
    main_title = 24
    pane_title = 18
    pane_text = 16
    plt.suptitle("Network Traffic", fontsize = main_title)
    ax[0].set_title("Inbound", fontsize = pane_title)
    ax[0].set_xlim((-180.0, 180.0))
    ax[0].set_xlabel("Longitude", fontsize = pane_text)
    ax[0].set_ylim((-90.0, 90.0))
    ax[0].set_ylabel("Latitude", fontsize = pane_text)
    ax[0].scatter(lons, lats, marker = ",", s = 1, alpha = 0.10, color = "black")
    #
    # the traffic direction vectors...
    #
    print("...inbound traffic vectors")
    for i in tqdm(range(len(bps))):
        if (traffic_color[i] == "green"):
            ax[0].plot([slatlon[i][0], dlatlon[i][0]], [slatlon[i][1], dlatlon[i][1]],
                       color = traffic_color[i], lw = dur[i], alpha = bps[i])
    #
    # the outbound traffic map...
    #
    worldmap = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
    worldmap.plot(color = "lightgrey", ax = ax[1])
    #
    # the various endpoints...
    #
    ax[1].set_title("Outbound", size = pane_title)
    ax[1].set_xlim((-180.0, 180.0))
    ax[1].set_xlabel("Longitude", size = pane_text)
    ax[1].set_ylim((-90.0, 90.0))
    ax[1].set_ylabel("Latitude", size = pane_text)
    ax[1].scatter(lons, lats, marker = ",", s = 1, alpha = 0.10, color = "black")
    #
    # the traffic direction vectors...
    #
    print("...outbound traffic vectors")
    for i in tqdm(range(len(bps))):
        if (traffic_color[i] == "red"):
            ax[1].plot([slatlon[i][0], dlatlon[i][0]], [slatlon[i][1], dlatlon[i][1]],
                       color = traffic_color[i], lw = dur[i], alpha = bps[i])
    plt.savefig(os.path.join(places("images"), "all_traffic.png"))
    if (show_world):
        plt.show()
    else:
        plt.close()
    return None

if (__name__ == "__main__"):
    """
    """
    world_graphics = True
    metrics_graphics = True
    print("")
    #
    # load the addresses cache...
    #
    print("load addresses cache...")
    cache = Cache()
    keys = sorted(list(cache.data.keys()))
    lats = [cache.data[key]["lat"] for key in keys]
    lons = [cache.data[key]["lon"] for key in keys]
    print(f"...loaded {len(keys)} addresses")
    #
    # load the traffic data...
    #
    print("load traffic data...")
    traffic = loader()
    print(f"...loaded {len(traffic)} records")
    #
    # sort the data to find traffic...
    #
    UNI_LATLON = (-76.60532, 2.44091)
    slatlon = []
    dlatlon = []
    bps = []
    dur = []
    traffic_color = []
    traffic_proto = []
    num_records = len(traffic)
    for i in tqdm(range(num_records)):
        sip = traffic['Source.IP'].values[i]
        dip = traffic['Destination.IP'].values[i]
        keeper = False
        if (public_address(sip)) and (not public_address(dip)):
            # this is INBOUND traffic...
            keeper = True
            cache.search(sip)
            traffic_color.append("green")
            slatlon.append((cache.data[sip]["lon"], cache.data[sip]["lat"]))
            dlatlon.append(UNI_LATLON)
        elif (not public_address(sip)) and (public_address(dip)):
            # this is OUTBOUND traffic...
            keeper = True
            cache.search(dip)
            traffic_color.append("red")
            slatlon.append(UNI_LATLON)
            dlatlon.append((cache.data[dip]["lon"], cache.data[dip]["lat"]))
        #
        # now if this *is* a keeper let's append various things...
        #
        if (keeper):
            bps.append(traffic['Flow.Bytes.s'].values[i])
            dur.append(traffic['Flow.Duration'].values[i])
            traffic_proto.append(traffic['ProtocolName'].values[i])
    #
    # status update...
    #
    print(f"...recorded data for {len(slatlon)} transactions")
    #
    # transparency of line will be based on traffic volume...
    #
    bps = [math.log10(b+10) for b in bps]
    bps_max = np.max(bps)
    bps = [b/bps_max for b in bps]
    print(f"normalized bps = ({np.min(bps)}, {np.median(bps)}, {np.max(bps)})")
    #
    # width of line will be based on duration of transaction...
    #
    dur = [math.log10(d+10) for d in dur]
    dur_max = np.max(dur)
    dur = [d/dur_max for d in dur]
    print(f"normalized dur = ({np.min(dur)}, {np.median(dur)}, {np.max(dur)})")
    print("")
    #
    # perhaps do pretty graphics...
    #
    if (world_graphics):
        display_world(slatlon, dlatlon, traffic_color, dur, bps, show_world = True)
    #
    # get the traffic protocol ranking...
    #
    ranking = traffic_proto_ranking(traffic_proto)
    #
    # nearest integer function because (incredibly) there is none in numpy...
    #
    def nint(x:float):
        return int(x + 0.5)
    pct_total = 0.0
    population = {}
    for i in range(0, len(ranking)):
        (percentage, proto) = ranking[i]
        chance = nint(100.0 / percentage)
        pct_total += percentage
        print("pct_total: %9.5f%%, 1/likelihood: %6d, cumulative_pct: %9.5f%%, count: %6d, proto: '%s'" %
              (percentage, chance, pct_total, int((percentage/100)*len(dur)), proto))
        population[proto] = {
            "rank":i,
            "pct_total":pct_total,
            "inv_likelihood": chance,
            "cumulative_pct":pct_total,
            "metrics":{
                "path":{
                    "src":[],
                    "dst":[],
                },
                "flowrate":{
                    "data":[],
                    "count":0,
                    "mode":-1,
                    "median":-1,
                    "mean":-1,
                    "std":-1,
                    "threshold":-1,
                },
                "duration":{
                    "data":[],
                    "count":0,
                    "mode":-1,
                    "median":-1,
                    "mean":-1,
                    "std":-1,
                    "threshold":-1,
                },
                "volume":{
                    "data":[],
                    "count":0,
                    "mode":-1,
                    "median":-1,
                    "mean":-1,
                    "std":-1,
                    "threshold":-1,
                },
                "avpktsz":{ #"Average.Packet.Size"
                    "data":[],
                    "count":0,
                    "mode":-1,
                    "median":-1,
                    "mean":-1,
                    "std":-1,
                    "threshold":-1,
                },
                "dnuprat":{#"Down.Up.Ratio"
                    "data":[],
                    "count":0,
                    "mode":-1,
                    "median":-1,
                    "mean":-1,
                    "std":-1,
                    "threshold":-1,
                },
                "pktlenvar":{#"Packet.Length.Variance"
                    "data":[],
                    "count":0,
                    "mode":-1,
                    "median":-1,
                    "mean":-1,
                    "std":-1,
                    "threshold":-1,
                },
                "fwdpktlen":{#"Forward.Packet.Length.Mean"
                    "data":[],
                    "count":0,
                    "mode":-1,
                    "median":-1,
                    "mean":-1,
                    "std":-1,
                    "threshold":-1,
                },
                "bwdpktlen":{#"Backward.Packet.Length.Mean"
                    "data":[],
                    "count":0,
                    "mode":-1,
                    "median":-1,
                    "mean":-1,
                    "std":-1,
                    "threshold":-1,
                },
                "actmean":{#"Active.Mean"
                    "data":[],
                    "count":0,
                    "mode":-1,
                    "median":-1,
                    "mean":-1,
                    "std":-1,
                    "threshold":-1,
                },
            },
        }
    #
    # now compute population metrics by walking through the traffic data...
    #
    print("\n...gathering population metrics data for flowrate and duration as function of protocol")
    for i in tqdm(range(len(traffic))):
        proto     = traffic['ProtocolName'].values[i]
        
        flowrate  = traffic['Flow.Bytes.s'].values[i]
        duration  = traffic['Flow.Duration'].values[i]
        avpktsz   = traffic["Average.Packet.Size"].values[i]
        dnuprat   = traffic["Down.Up.Ratio"].values[i]
        pktlenvar = traffic["Packet.Length.Variance"].values[i]
        volume    = flowrate * duration
        fwdpktlen = traffic["Fwd.Packet.Length.Mean"].values[i]
        bwdpktlen = traffic["Bwd.Packet.Length.Mean"].values[i]
        actmean   = traffic["Active.Mean"].values[i]
        sip       = traffic['Source.IP'].values[i]
        dip       = traffic['Destination.IP'].values[i]
        if ((public_address(sip) and not public_address(dip)) or
            ((not public_address(sip)) and public_address(dip))):
            #
            # then it's an off-site transaction... so we can work with it...
            #
            population[proto]["metrics"]["flowrate"]["data"].append(flowrate)
            population[proto]["metrics"]["duration"]["data"].append(duration)
            population[proto]["metrics"]["volume"]["data"].append(volume)
            population[proto]["metrics"]["avpktsz"]["data"].append(avpktsz)
            population[proto]["metrics"]["dnuprat"]["data"].append(dnuprat)
            population[proto]["metrics"]["pktlenvar"]["data"].append(pktlenvar)
            population[proto]["metrics"]["fwdpktlen"]["data"].append(fwdpktlen)
            population[proto]["metrics"]["bwdpktlen"]["data"].append(bwdpktlen)
            population[proto]["metrics"]["actmean"]["data"].append(actmean)
            if (public_address(sip) and (not public_address(dip))):
                population[proto]["metrics"]["path"]["src"].append((cache.data[sip]["lon"], cache.data[sip]["lat"]))
                population[proto]["metrics"]["path"]["dst"].append(UNI_LATLON)
            elif ((not public_address(sip)) and public_address(dip)):
                population[proto]["metrics"]["path"]["src"].append(UNI_LATLON)
                population[proto]["metrics"]["path"]["dst"].append((cache.data[dip]["lon"], cache.data[dip]["lat"]))
    #
    # compute key statistics regarding the metrics...
    #
    print("...computing population metrics")
    for proto in population.keys():
        #
        # flowrate...
        #
        population[proto]["metrics"]["flowrate"]["count"]  = len(population[proto]["metrics"]["flowrate"]["data"])
        population[proto]["metrics"]["flowrate"]["threshold"] = 1.0 / float(population[proto]["metrics"]["flowrate"]["count"])
        population[proto]["metrics"]["flowrate"]["mode"]   = mode(population[proto]["metrics"]["flowrate"]["data"]).mode[0]
        population[proto]["metrics"]["flowrate"]["median"] = np.median(population[proto]["metrics"]["flowrate"]["data"])
        population[proto]["metrics"]["flowrate"]["mean"]   = np.mean(population[proto]["metrics"]["flowrate"]["data"])
        population[proto]["metrics"]["flowrate"]["std"]    = np.std(population[proto]["metrics"]["flowrate"]["data"])
        #
        # duration...
        #
        population[proto]["metrics"]["duration"]["count"]  = len(population[proto]["metrics"]["duration"]["data"])
        population[proto]["metrics"]["duration"]["threshold"] = 1.0 / float(population[proto]["metrics"]["duration"]["count"])
        population[proto]["metrics"]["duration"]["mode"]   = mode(population[proto]["metrics"]["duration"]["data"]).mode[0]
        population[proto]["metrics"]["duration"]["median"] = np.median(population[proto]["metrics"]["duration"]["data"])
        population[proto]["metrics"]["duration"]["mean"]   = np.mean(population[proto]["metrics"]["duration"]["data"])
        population[proto]["metrics"]["duration"]["std"]    = np.std(population[proto]["metrics"]["duration"]["data"])
        #
        # volume...
        #
        population[proto]["metrics"]["volume"]["count"]  = len(population[proto]["metrics"]["volume"]["data"])
        population[proto]["metrics"]["volume"]["threshold"] = 1.0 / float(population[proto]["metrics"]["volume"]["count"])
        population[proto]["metrics"]["volume"]["mode"]   = mode(population[proto]["metrics"]["volume"]["data"]).mode[0]
        population[proto]["metrics"]["volume"]["median"] = np.median(population[proto]["metrics"]["volume"]["data"])
        population[proto]["metrics"]["volume"]["mean"]   = np.mean(population[proto]["metrics"]["volume"]["data"])
        population[proto]["metrics"]["volume"]["std"]    = np.std(population[proto]["metrics"]["volume"]["data"])
        #
        # avpktsz...
        #
        population[proto]["metrics"]["avpktsz"]["count"]  = len(population[proto]["metrics"]["avpktsz"]["data"])
        population[proto]["metrics"]["avpktsz"]["threshold"] = 1.0 / float(population[proto]["metrics"]["avpktsz"]["count"])
        population[proto]["metrics"]["avpktsz"]["mode"]   = mode(population[proto]["metrics"]["avpktsz"]["data"]).mode[0]
        population[proto]["metrics"]["avpktsz"]["median"] = np.median(population[proto]["metrics"]["avpktsz"]["data"])
        population[proto]["metrics"]["avpktsz"]["mean"]   = np.mean(population[proto]["metrics"]["avpktsz"]["data"])
        population[proto]["metrics"]["avpktsz"]["std"]    = np.std(population[proto]["metrics"]["avpktsz"]["data"])
        #
        # dnuprat...
        #
        population[proto]["metrics"]["dnuprat"]["count"]  = len(population[proto]["metrics"]["dnuprat"]["data"])
        population[proto]["metrics"]["dnuprat"]["threshold"] = 1.0 / float(population[proto]["metrics"]["dnuprat"]["count"])
        population[proto]["metrics"]["dnuprat"]["mode"]   = mode(population[proto]["metrics"]["dnuprat"]["data"]).mode[0]
        population[proto]["metrics"]["dnuprat"]["median"] = np.median(population[proto]["metrics"]["dnuprat"]["data"])
        population[proto]["metrics"]["dnuprat"]["mean"]   = np.mean(population[proto]["metrics"]["dnuprat"]["data"])
        population[proto]["metrics"]["dnuprat"]["std"]    = np.std(population[proto]["metrics"]["dnuprat"]["data"])
        #
        # fwdpktlen...
        #
        population[proto]["metrics"]["fwdpktlen"]["count"]  = len(population[proto]["metrics"]["fwdpktlen"]["data"])
        population[proto]["metrics"]["fwdpktlen"]["threshold"] = 1.0 / float(population[proto]["metrics"]["fwdpktlen"]["count"])
        population[proto]["metrics"]["fwdpktlen"]["mode"]   = mode(population[proto]["metrics"]["fwdpktlen"]["data"]).mode[0]
        population[proto]["metrics"]["fwdpktlen"]["median"] = np.median(population[proto]["metrics"]["fwdpktlen"]["data"])
        population[proto]["metrics"]["fwdpktlen"]["mean"]   = np.mean(population[proto]["metrics"]["fwdpktlen"]["data"])
        population[proto]["metrics"]["fwdpktlen"]["std"]    = np.std(population[proto]["metrics"]["fwdpktlen"]["data"])

        #
        # avpktsz...
        #
        population[proto]["metrics"]["bwdpktlen"]["count"]  = len(population[proto]["metrics"]["bwdpktlen"]["data"])
        population[proto]["metrics"]["bwdpktlen"]["threshold"] = 1.0 / float(population[proto]["metrics"]["bwdpktlen"]["count"])
        population[proto]["metrics"]["bwdpktlen"]["mode"]   = mode(population[proto]["metrics"]["bwdpktlen"]["data"]).mode[0]
        population[proto]["metrics"]["bwdpktlen"]["median"] = np.median(population[proto]["metrics"]["bwdpktlen"]["data"])
        population[proto]["metrics"]["bwdpktlen"]["mean"]   = np.mean(population[proto]["metrics"]["bwdpktlen"]["data"])
        population[proto]["metrics"]["bwdpktlen"]["std"]    = np.std(population[proto]["metrics"]["bwdpktlen"]["data"])
        #
        # dnuprat...
        #
        population[proto]["metrics"]["actmean"]["count"]  = len(population[proto]["metrics"]["actmean"]["data"])
        population[proto]["metrics"]["actmean"]["threshold"] = 1.0 / float(population[proto]["metrics"]["actmean"]["count"])
        population[proto]["metrics"]["actmean"]["mode"]   = mode(population[proto]["metrics"]["actmean"]["data"]).mode[0]
        population[proto]["metrics"]["actmean"]["median"] = np.median(population[proto]["metrics"]["actmean"]["data"])
        population[proto]["metrics"]["actmean"]["mean"]   = np.mean(population[proto]["metrics"]["actmean"]["data"])
        population[proto]["metrics"]["actmean"]["std"]    = np.std(population[proto]["metrics"]["actmean"]["data"])
        #
        # pktlenvar...
        #
        population[proto]["metrics"]["pktlenvar"]["count"]  = len(population[proto]["metrics"]["pktlenvar"]["data"])
        population[proto]["metrics"]["pktlenvar"]["threshold"] = 1.0 / float(population[proto]["metrics"]["pktlenvar"]["count"])
        population[proto]["metrics"]["pktlenvar"]["mode"]   = mode(population[proto]["metrics"]["pktlenvar"]["data"]).mode[0]
        population[proto]["metrics"]["pktlenvar"]["median"] = np.median(population[proto]["metrics"]["pktlenvar"]["data"])
        population[proto]["metrics"]["pktlenvar"]["mean"]   = np.mean(population[proto]["metrics"]["pktlenvar"]["data"])
        population[proto]["metrics"]["pktlenvar"]["std"]    = np.std(population[proto]["metrics"]["pktlenvar"]["data"])

    #
    # now perhaps show a table summarizing some of the metrics...
    #
    if (metrics_graphics):
        display_metrics(population,
                        min_count = 100, # probably 100 for production...
                        num_bins = 10,  # still experimenting...
                        show_histograms = False,
                        show_table = True,
        )

    dill.dump(population,
              gzip.open(os.path.join(places("datasets"),
                                     "population_metrics.dill"), "wb"))
    
