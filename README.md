# Blueprint Accelerator: Anomaly Detection with DNS Data, AI and Databricks

## Overview
This is an accelerator for the anomaly detection module of a **N**etwork **T**hreat **D**etection **S**ystem (NTDS) for detecting security threats to a computer network based on recognition of unusual activity observed in the network’s traffic.


## About The Data
In developing this anomaly detection module, a freely available dataset from the Kaggle website (called “Dataset-Unicauca-Version2-87Atts”) was used in lieu of a streaming data source. This dataset consists of several million rows of data captured at the Universidad del Cauca in Columbia over portions of two months in 2017. The data contains 87 columns of statistical data characterizing the network traffic observed at the University’s data center and has been labeled according traffic protocol types.

The data is separated into purely internal (between locations within the university network) and external (either traffic flowing into the university or traffic flowing out from the university). This separation involved sifting through the several million records, identifying external “ip-addresses” and determinine the resulting “geo-location” meta data for each address. There were 21,000+ external addresses in the dataset. Then for each traffic protocol (Google, Facebook, MSN, Yahoo, Signal, Twitter, etc) various statistical measures are computed and outlier transactions are identified. Depending on the volume of traffic for the particular protocol this may be as unsual as 1/100,000 events or as (relatively) common as 1/1,000. For each protocol geographic distribution maps are created identifying the traffic vectors. Sample reports for selected protocols are presented.

## Special Thanks
This module builds upon an existing Databricks accelerator called “[Threat Detection by DNS](https://databricks.com/solutions/accelerators/threat-detection)”. The original Databricks accelerator attempts to recognize instances where the plain-text DNS descriptors for network locations have been mangled in known ways (e.g. appel.com for apple.com, facebook.com.tv for facebook.com etc) that have been associated with phishing scams. This module had originally been the intention to improve upon that accelerator, but that approach relies on published tables of known manglings and is largely limited to mitigating against typos and phishing.

The original version of this accelerator was created as an entry for Blueprint Technologies' X-Challenge. X-Challenges are designed to provide challenges that enable Blueprinters, through technical experimentation & exploration, to participate in a broad range of strategic initiatives.
