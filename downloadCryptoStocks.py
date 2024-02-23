import numpy as np
from statsmodels.regression.rolling import RollingOLS
import pandas as pd
import yfinance as yf
from technical_analysis_calculations import Calculations
import pandas_datareader.data as web
import statsmodels.api as sm
from sklearn.cluster import KMeans
import re

#prepare for downloading stocks
stocks = []
def collect_crypto_data(string):
    pattern = re.compile(r'[A-Z][A-Z]+', re.DOTALL)
    matches = pattern.findall(string)
    result = []

    for match in matches:
        result.append(match)

    return result


def remove_duplicates(arr):
    unique_elements = set()

    result = []

    for element in arr:
        if element not in unique_elements:
            unique_elements.add(element)
            result.append(element)

    return result


symbols = 'Bitcoin Bitcoin BTC $1,001,272,998,765  $50,992.61 19,635,650 BTC	$24,192,279,767	 0.28% -1.12% -1.91% 2 Ethereum Ethereum ETH $352,207,440,311  $2,931.19 120,158,442 ETH * $14,881,631,437	 0.31% -1.67% 5.57% 3 Tether USDt Tether USDt USDT $97,828,263,604  $0.9998 97,843,287,089 USDT * $53,825,394,264	 <0.01% 0.02% -0.05% 4 BNB BNB BNB $55,853,546,654  $373.49 149,543,453 BNB * $1,790,999,324	 0.78% -1.45% 4.55% 5 Solana Solana SOL $44,316,753,239  $100.50 440,960,958 SOL * $1,691,871,600	 1.00% -3.71% -8.04% 6 XRP XRP XRP $29,126,556,297  $0.5339 54,558,598,490 XRP * $1,198,360,218	 0.89% -1.49% -5.12% 7 USDC USDC USDC $28,049,853,298  $1.00 28,049,234,160 USDC * $5,565,639,828	 0.01% <0.01% <0.01% 8 Cardano Cardano ADA $20,614,360,332  $0.5812 35,467,219,208 ADA * $476,889,657	 1.43% -1.99% -1.48% 9 Avalanche Avalanche AVAX $13,582,159,670  $36.01 377,169,545 AVAX * $497,969,814	 1.22% -3.21% -10.22% 10 TRON TRON TRX $12,190,173,419  $0.1385 88,017,270,761 TRX * $289,803,919	 0.23% -0.71% 5.28% 11 Dogecoin Dogecoin DOGE $12,097,536,733  $0.08448 143,193,436,384 DOGE	$392,859,852	 0.88% -0.25% -0.75% 12 Chainlink Chainlink LINK $10,520,806,904  $17.92 587,099,970 LINK * $461,245,965	 0.84% -2.73% -7.76% 13 Polkadot Polkadot DOT $9,630,609,990  $7.48 1,287,581,836 DOT * $258,462,654	 1.72% -1.38% -1.65% 14 Polygon Polygon MATIC $9,321,169,461  $0.9691 9,618,312,865 MATIC * $841,707,669	 1.88% -0.07% 5.33% 15 Toncoin Toncoin TON $7,227,547,116  $2.08 3,467,316,729 TON * $36,018,649	 0.45% -0.49% -4.89% 16 Uniswap Uniswap UNI $6,577,713,594  $11.00 598,187,016 UNI * $1,444,242,929	 -1.21% 47.98% 49.00% 17 Internet Computer Internet Computer ICP $5,668,488,840  $12.34 459,372,771 ICP * $118,028,426	 1.36% -4.65% -5.60% 18 Shiba Inu Shiba Inu SHIB $5,621,640,489  $0.00000954 589,289,732,858,420 SHIB * $149,937,921	 1.10% -0.81% -2.12% 19 Dai Dai DAI $5,348,263,483  $1.00 5,347,888,596 DAI * $127,474,311	 <0.01% 0.03% 0.02% 20 Bitcoin Cash Bitcoin Cash BCH $5,189,893,017  $264.12 19,649,906 BCH	$196,956,601	 0.88% 0.84% -3.62% 21 Litecoin Litecoin LTC $5,091,430,175  $68.58 74,237,794 LTC	$279,357,074	 0.87% -1.09% -1.53% 22 Immutable Immutable IMX $4,366,766,319  $3.14 1,389,224,659 IMX * $96,259,995	 1.30% -5.56% 0.04% 23 Filecoin Filecoin FIL $4,136,000,416  $8.05 514,043,137 FIL	$897,052,125	 0.45% -1.68% 41.16% 24 Cosmos Cosmos ATOM $3,841,041,433  $9.91 387,724,311 ATOM * $165,219,064	 1.33% 0.60% -2.05% 25 UNUS SED LEO UNUS SED LEO LEO $3,823,960,975  $4.12 927,395,329 LEO * $1,821,753	 -0.44% -0.29% 1.24% 26 Ethereum Classic Ethereum Classic ETC $3,723,006,951  $25.55 145,699,817 ETC	$173,255,982	 1.19% -1.27% -3.72% 27 Kaspa Kaspa KAS $3,720,597,292  $0.1633 22,787,255,930 KAS	$51,630,193	 0.74% -4.13% 13.38% 28 Hedera Hedera HBAR $3,717,825,216  $0.1104 33,679,155,196 HBAR * $239,277,912	 2.29% -4.35% 32.20% 29 Stacks Stacks STX $3,559,154,968  $2.47 1,443,322,746 STX	$204,074,688	 1.81% -4.52% -2.42% 30 Optimism Optimism OP $3,444,342,031  $3.60 957,378,568 OP * $216,763,827	 1.87% -1.40% -0.80% 31 NEAR Protocol NEAR Protocol NEAR $3,424,092,422  $3.29 1,041,490,197 NEAR * $199,483,670	 2.97% 1.70% 1.36% 32 Aptos Aptos APT $3,348,200,454  $9.14 366,420,577 APT * $124,481,030	 1.66% -2.07% -7.18% 33 First Digital USD First Digital USD FDUSD $3,312,282,662  $1.00 3,306,729,237 FDUSD * $6,017,742,220	 0.00% -0.18% 0.12% 34 Stellar Stellar XLM $3,272,919,938  $0.115 28,457,243,394 XLM * $84,471,368	 1.07% -0.34% 0.65% 35 VeChain VeChain VET $3,202,489,308  $0.04404 72,714,516,834 VET * $107,173,332	 1.23% -1.02% -4.68% 36 Injective Injective INJ $3,091,573,555  $33.10 93,400,000 INJ * $177,037,294	 1.93% -5.40% -2.75% 37 OKB OKB OKB $3,037,782,238  $50.63 60,000,000 OKB * $6,087,402	 0.61% -0.89% -1.50% 38 Render Render RNDR $2,792,312,690  $7.38 378,257,447 RNDR * $468,454,003	 2.47% -3.83% 36.66% 39 Lido DAO Lido DAO LDO $2,781,513,428  $3.12 890,933,022 LDO * $127,417,015	 1.98% 3.32% -2.55% 40 Celestia Celestia TIA $2,701,872,916  $16.25 166,249,007 TIA * $154,288,523	 1.88% -5.29% -10.89% 41 The Graph The Graph GRT $2,568,554,267  $0.2728 9,417,218,451 GRT * $380,489,080	 1.73% -3.87% 40.23% 42 Mantle Mantle MNT $2,525,528,977  $0.7826 3,226,917,893 MNT * $144,805,641	 0.55% 1.58% 0.33% 43 Cronos Cronos CRO $2,309,653,362  $0.09142 25,263,013,692 CRO * $13,173,832	 0.74% -0.78% 1.83% 44 Arbitrum Arbitrum ARB $2,272,183,362  $1.78 1,275,000,000 ARB * $401,259,315	 1.68% -3.52% -10.73% 45 Monero Monero XMR $2,249,596,339  $122.25 18,401,566 XMR	$104,052,767	 0.70% -0.89% -1.19% 46 Sei Sei SEI $2,032,501,393  $0.7971 2,550,000,000 SEI * $302,551,082	 1.24% -6.37% -13.66% 47 Sui Sui SUI $1,865,514,970  $1.60 1,165,931,966 SUI * $491,343,772	 1.31% -6.50% -10.28% 48 Maker Maker MKR $1,833,531,830  $1,985.89 923,281 MKR * $64,944,465	 1.10% -2.39% -3.85% 49 THORChain THORChain RUNE $1,724,978,594  $5.06 341,160,501 RUNE * $168,250,872	 1.21% -1.42% -11.18% 50 Beam Beam BEAM $1,681,719,886  $0.03245 51,818,745,148 BEAM * $53,442,461	 1.28% -2.98% 17.52% 51 Algorand Algorand ALGO $1,504,541,782  $0.1869 8,047,843,472 ALGO * $46,743,550	 1.66% -1.81% -2.70% 52 MultiversX MultiversX EGLD $1,502,150,080  $56.45 26,608,658 EGLD * $25,942,937	 1.33% -3.29% -4.03% 53 Flow Flow FLOW $1,480,579,609  $0.9932 1,490,653,079 FLOW * $139,192,888	 3.30% 6.68% 4.45% 54 Bitcoin SV Bitcoin SV BSV $1,458,755,771  $74.26 19,642,638 BSV	$59,869,786	 1.07% -2.11% -4.93% 55 Flare Flare FLR $1,418,022,984  $0.04105 34,541,962,829 FLR * $85,959,545	 7.49% 20.73% 30.65% 56 Aave Aave AAVE $1,400,804,934  $95.03 14,740,073 AAVE * $214,470,646	 1.19% 3.04% 3.80% 57 Starknet Starknet STRK $1,399,163,712  $1.92 728,000,000 STRK * $995,866,466	 0.65% 4.71% -18.14% 58 Bitget Token Bitget Token BGB $1,390,172,361  $0.993 1,400,000,000 BGB * $29,872,844	 0.62% -1.57% -2.35% 59 Mina Mina MINA $1,319,360,783  $1.25 1,057,310,810 MINA * $40,820,855	 0.90% -2.63% -8.48% 60 Helium Helium HNT $1,314,646,840  $8.17 160,875,442 HNT	$21,477,452	 1.39% -10.39% -15.11% 61 ORDI ORDI ORDI $1,259,275,947  $59.97 21,000,000 ORDI * $207,680,867	 1.78% -7.87% -12.99% 62 TrueUSD TrueUSD TUSD $1,256,967,990  $0.9756 1,288,456,472 TUSD * $87,736,873	 0.04% -0.09% -0.26% 63 Quant Quant QNT $1,243,253,616  $102.98 12,072,738 QNT * $23,399,721	 0.90% -0.42% -6.68% 64 Theta Network Theta Network THETA $1,195,892,826  $1.20 1,000,000,000 THETA * $29,622,446	 1.81% -1.60% 7.23% 65 Synthetix Synthetix SNX $1,159,209,007  $3.81 304,620,395 SNX * $67,383,222	 5.12% 7.08% 6.10% 66 The Sandbox The Sandbox SAND $1,121,337,893  $0.5011 2,237,731,926 SAND * $105,786,264	 2.24% 1.10% 2.44% 67 Chiliz Chiliz CHZ $1,120,399,192  $0.1261 8,888,290,622 CHZ * $101,331,950	 1.38% -3.11% 12.99% 68 Worldcoin Worldcoin WLD $1,114,957,906  $8.33 133,888,487 WLD * $1,096,549,812	 1.49% -2.52% 88.95% 69 Siacoin Siacoin SC $1,113,565,267  $0.01971 56,488,842,155 SC	$284,500,437	 0.65% 15.25% 50.99% 70 Fantom Fantom FTM $1,108,180,991  $0.3953 2,803,634,836 FTM * $65,044,307	 1.64% -4.23% -2.56% 71 Axie Infinity Axie Infinity AXS $1,070,110,301  $7.78 137,505,315 AXS * $78,263,745	 2.02% -0.32% -2.60% 72 Tezos Tezos XTZ $1,065,355,687  $1.10 971,899,635 XTZ * $34,595,465	 2.18% -2.17% 3.39% 73 BitTorrent (New) BitTorrent (New) BTT $1,034,953,216  $0.000001069 968,246,428,571,000 BTT * $44,866,630	 0.68% -1.66% 3.46% 74 SingularityNET SingularityNET AGIX $1,024,690,310  $0.8154 1,256,596,283 AGIX * $470,205,043	 8.42% 13.21% 106.68% 75 KuCoin Token KuCoin Token KCS $1,013,084,659  $10.50 96,496,827 KCS * $3,489,984	 -0.75% -1.39% 1.20% 76 ApeCoin ApeCoin APE $1,007,056,030  $1.66 604,895,833 APE * $57,530,786	 1.87% -2.00% 2.87% 77 EOS EOS EOS $949,840,499  $0.8495 1,118,082,450 EOS * $165,996,970	 10.95% 10.38% 11.85% 78 Blur Blur BLUR $944,644,257  $0.6609 1,429,344,117 BLUR * $95,103,190	 1.77% -5.54% -6.10% 79 SATS SATS 1000SATS $940,715,604  $0.000448 2,100,000,000,000 1000SATS * $39,621,048	 1.63% -6.56% -14.85% 80 dYdX (ethDYDX) dYdX (ethDYDX) ETHDYDX $939,967,307  $3.18 295,616,430 ETHDYDX * $203,450,017	 1.24% 7.90% 3.29% 81 Dymension Dymension DYM $939,747,164  $6.44 146,000,000 DYM * $99,430,541	 1.22% -10.41% -15.61% 82 Decentraland Decentraland MANA $913,075,053  $0.4823 1,893,095,371 MANA * $78,677,303	 1.73% -0.78% -2.08% 83 Fetch.ai Fetch.ai FET $899,504,858  $1.08 832,262,598 FET * $336,940,571	 0.48% -8.20% 50.99% 84 Astar Astar ASTR $888,849,140  $0.1597 5,565,629,313 ASTR * $24,625,446	 1.41% -2.28% -5.66% 85 Akash Network Akash Network AKT $884,947,116  $3.87 228,624,295 AKT * $6,296,667	 -0.21% -4.89% 12.78% 86 Neo Neo NEO $881,113,312  $12.49 70,538,831 NEO * $31,630,920	 2.04% -0.13% -3.40% 87 Conflux Conflux CFX $876,472,976  $0.2338 3,748,309,390 CFX	$54,318,076	 1.43% -4.60% 1.13% 88 Ronin Ronin RON $869,178,348  $2.91 298,799,748 RON * $102,349,637	 0.91% -8.30% -0.82% 89 Arweave Arweave AR $852,601,474  $13.03 65,454,185 AR * $53,181,368	 0.12% -5.80% 10.77% 90 WOO WOO WOO $838,534,246  $0.4584 1,829,389,584 WOO * $52,572,643	 1.06% -2.65% 15.55% 91 Kava Kava KAVA $837,809,555  $0.7737 1,082,861,683 KAVA * $35,351,973	 1.21% -0.88% 4.28% 92 IOTA IOTA IOTA $837,490,430  $0.2656 3,152,954,445 IOTA * $19,905,139	 2.41% -2.68% -0.96% 93 Axelar Axelar AXL $828,306,305  $1.44 575,946,173 AXL * $22,526,639	 0.65% 0.83% 17.35% 94 Pyth Network Pyth Network PYTH $819,376,583  $0.5399 1,517,569,218 PYTH * $89,861,541	 1.48% -4.19% -7.95% 95 Gnosis Gnosis GNO $805,926,806  $311.22 2,589,588 GNO * $6,686,733	 0.20% -1.14% 10.42% 96 Oasis Network Oasis Network ROSE $798,746,611  $0.119 6,713,599,876 ROSE * $53,133,276	 2.18% -2.01% -0.83% 97 Gala Gala GALA $795,998,227  $0.02863 27,799,861,148 GALA * $102,374,228	 3.16% -1.09% 8.46% 98 Klaytn Klaytn KLAY $769,922,531  $0.2204 3,492,857,908 KLAY * $21,654,981	 1.01% -0.55% 0.11% 99 Osmosis Osmosis OSMO $756,897,030  $1.54 492,590,761 OSMO * $42,106,307	 1.16% -0.54% -3.45% 100 Manta Network Manta Network MANTA $754,289,395  $3.01 251,000,000 MANTA * $252,051,655	 0.85% -9.72% 2.55% 101 USDD USDD USDD $737,333,355  $0.9984 738,478,575 USDD * $13,800,529	 0.02% -0.04% 0.11% 102 WEMIX WEMIX WEMIX $734,499,084  $2.03 362,605,491 WEMIX * $2,982,459	 0.33% -1.50% -9.86% 103 PancakeSwap PancakeSwap CAKE $730,719,412  $3.10 235,424,822 CAKE * $228,397,569	 1.45% 9.77% 13.39% 104 Bonk Bonk BONK $725,661,244  $0.00001146 63,333,513,043,628 BONK * $77,513,462	 1.84% -3.48% -12.85% 105 Terra Classic Terra Classic LUNC $695,088,156  $0.0001204 5,774,924,946,208 LUNC * $44,187,219	 1.46% -1.56% -3.85% 106 Jupiter Jupiter JUP $660,398,464  $0.4892 1,350,000,000 JUP * $244,374,785	 2.83% 2.75% -4.05% 107 JasmyCoin JasmyCoin JASMY $652,290,586  $0.01323 49,299,999,677 JASMY * $556,126,991	 3.06% -15.73% 111.87% 108 Curve DAO Token Curve DAO Token CRV $651,414,176  $0.5795 1,124,045,187 CRV * $109,894,227	 1.01% 4.17% 9.44% 109 Ethereum Name Service Ethereum Name Service ENS $648,862,217  $21.07 30,795,296 ENS * $72,534,596	 1.64% -2.32% -3.46% 110 Nexo Nexo NEXO $646,851,686  $1.16 560,000,011 NEXO * $3,441,494	 0.84% 0.06% 9.36% 111 eCash eCash XEC $638,440,184  $0.0000325 19,642,879,673,092 XEC * $10,550,394	 1.37% -0.90% -3.34% 112 Pendle Pendle PENDLE $636,941,904  $2.67 238,185,588 PENDLE * $70,459,666	 1.92% -1.53% -14.85% 113 Frax Share Frax Share FXS $636,506,430  $8.27 76,932,702 FXS * $27,213,502	 1.35% -1.90% -7.52% 114 Ondo Ondo ONDO $577,184,384  $0.4165 1,385,916,323 ONDO * $219,599,676	 6.98% -3.72% 62.49% 115 Altlayer Altlayer ALT $568,901,671  $0.5172 1,100,000,000 ALT * $245,364,137	 3.22% -8.92% 29.81% 116 XDC Network XDC Network XDC $567,805,142  $0.04085 13,899,638,989 XDC * $14,147,707	 0.05% -0.77% -5.54% 117 Core Core CORE $563,695,202  $0.65 867,207,536 CORE * $13,142,938	 1.25% 5.37% 20.31% 118 FTX Token FTX Token FTT $563,634,846  $1.71 328,895,104 FTT * $13,070,991	 0.54% -2.64% -5.25% 119 Rocket Pool Rocket Pool RPL $551,746,904  $27.39 20,141,647 RPL * $4,672,031	 0.55% -1.65% -13.25% 120 1inch Network 1inch Network 1INCH $543,133,516  $0.4757 1,141,759,456 1INCH * $84,445,113	 2.25% 7.24% 6.40% 121 Trust Wallet Token Trust Wallet Token TWT $539,117,851  $1.29 416,649,900 TWT * $36,461,241	 1.23% 0.46% 6.03% 122 ZetaChain ZetaChain ZETA $529,264,143  $2.24 236,468,750 ZETA * $133,213,775	 3.77% -4.75% -10.88% 123 IoTeX IoTeX IOTX $529,033,711  $0.05603 9,441,378,955 IOTX * $23,191,298	 1.65% -2.49% 18.40% 124 Compound Compound COMP $525,091,812  $64.95 8,084,194 COMP * $133,320,055	 -1.32% 9.26% 12.36% 125 Pepe Pepe PEPE $514,684,400  $0.000001223 420,689,899,999,995 PEPE * $270,880,680	 2.11% 1.80% 5.27% 126 Tether Gold Tether Gold XAUt $501,648,455  $2,034.89 246,524 XAUt * $5,767,648	 0.20% 0.66% 1.32% 127 SuperVerse SuperVerse SUPER $465,377,326  $0.9541 487,776,093 SUPER * $35,756,611	 1.40% -8.52% -6.75% 128 Metis Metis METIS $461,867,937  $87.97 5,250,547 METIS * $47,936,229	 0.16% 1.51% 0.60% 129 Casper Casper CSPR $461,663,587  $0.03908 11,814,693,897 CSPR * $10,866,185	 0.71% -4.94% 3.86% 130 Radix Radix XRD $460,532,639  $0.04436 10,380,819,467 XRD * $4,432,395	 0.93% -7.11% 4.47% 131 Enjin Coin Enjin Coin ENJ $458,487,506  $0.3323 1,379,841,766 ENJ * $18,849,359	 1.60% -0.44% 2.52% 132 GateToken GateToken GT $455,277,709  $4.72 96,488,934 GT * $1,361,902	 0.35% 0.29% 0.69% 133 GMT GMT GMT $454,168,341  $0.2591 1,752,944,148 GMT * $47,041,517	 1.02% -2.25% -4.22% 134 aelf aelf ELF $450,849,196  $0.6302 715,360,021 ELF * $11,675,231	 0.47% -0.90% 2.71% 135 SKALE SKALE SKL $447,088,483  $0.0867 5,156,686,004 SKL * $19,288,279	 1.72% 1.27% -5.03% 136 Nervos Network Nervos Network CKB $446,489,702  $0.01024 43,594,965,195 CKB	$40,924,400	 0.21% -8.26% -7.89% 137 Zcash Zcash ZEC $445,171,591  $27.26 16,328,269 ZEC	$88,756,213	 1.05% -0.74% 22.09% 138 GMX GMX GMX $440,062,388  $46.53 9,456,727 GMX * $55,113,266	 1.89% 0.98% 5.49% 139 APENFT APENFT NFT $438,936,888  $0.0...04433 990,105,682,877,398 NFT * $35,084,984	 -0.06% -1.44% 0.75% 140 Terra Terra LUNA $436,457,132  $0.6545 666,830,720 LUNA * $27,817,992	 1.76% -1.76% -7.40% 141 Convex Finance Convex Finance CVX $431,276,203  $4.60 93,762,243 CVX * $10,476,232	 0.03% -3.26% 28.52% 142 Livepeer Livepeer LPT $431,413,592  $13.92 30,992,370 LPT * $73,915,252	 0.51% -7.44% -0.78% 143 Neutron Neutron NTRN $428,914,030  $1.54 278,805,850 NTRN * $18,272,586	 1.19% -6.24% -17.53% 144 Ocean Protocol Ocean Protocol OCEAN $428,405,456  $0.7537 568,381,103 OCEAN * $131,545,919	 1.32% -3.01% 42.32% 145 Bitcoin Gold Bitcoin Gold BTG $426,391,651  $24.35 17,513,924 BTG	$5,617,749	 0.22% -1.83% -6.53% 146 OriginTrail OriginTrail TRAC $424,136,426  $1.05 402,324,425 TRAC * $8,214,488	 4.94% 23.32% 43.00% 147 Gas Gas GAS $414,440,658  $6.21 66,788,855 GAS * $19,844,120	 1.61% -1.28% -4.11% 148 Mask Network Mask Network MASK $413,391,013  $4.31 96,025,000 MASK * $390,772,679	 -0.02% -3.10% 17.88% 149 Celo Celo CELO $413,379,860  $0.7831 527,877,912 CELO * $97,680,411	 1.39% 4.58% 5.24% 150 PAX Gold PAX Gold PAXG $405,711,122  $2,010.84 201,762 PAXG * $7,072,133	 0.35% 0.56% 1.18% 151 Holo Holo HOT $403,564,915  $0.002334 172,931,322,183 HOT * $17,683,171	 3.04% 0.32% 8.08% 152 Zilliqa Zilliqa ZIL $400,211,778  $0.02304 17,372,203,179 ZIL	$20,187,775	 1.79% -1.61% 1.10% 153 Xai Xai XAI $395,733,530  $1.43 277,118,150 XAI * $241,979,192	 4.82% 9.30% 45.51% 154 Pixels Pixels PIXEL $390,624,544  $0.5066 771,041,667 PIXEL * $195,388,003	 1.69% -5.62% -0.21% 155 Kusama Kusama KSM $385,597,559  $45.52 8,470,098 KSM * $21,371,734	 1.89% -2.32% 2.54% 156 Basic Attention Token Basic Attention Token BAT $368,723,608  $0.2474 1,490,413,701 BAT * $31,322,543	 1.62% -2.57% 2.26% 157 Illuvium Illuvium ILV $357,266,299  $94.83 3,767,377 ILV * $15,213,717	 1.49% -1.44% -1.82% 158 SafePal SafePal SFP $356,735,956  $0.7713 462,500,000 SFP * $4,415,993	 2.06% 1.07% 1.91% 159 Moonbeam Moonbeam GLMR $354,356,080  $0.4235 836,674,423 GLMR * $9,856,985	 0.60% -4.49% -1.54% 160 Loopring Loopring LRC $352,936,073  $0.2582 1,366,646,304 LRC * $22,558,084	 0.95% 0.31% 3.96% 161 VeThor Token VeThor Token VTHO $349,408,184  $0.004785 73,014,802,909 VTHO * $17,256,329	 2.29% -2.26% -0.59% 162 Dash Dash DASH $344,701,977  $29.52 11,677,099 DASH	$44,632,712	 1.89% -1.54% 2.99% 163 NEM NEM XEM $343,404,418  $0.03816 8,999,999,999 XEM * $8,029,246	 2.26% 1.23% 1.24% 164 Golem Golem GLM $341,707,221  $0.3417 1,000,000,000 GLM * $68,614,324	 1.74% -7.78% 53.28% 165 Qtum Qtum QTUM $337,420,353  $3.22 104,755,842 QTUM * $43,510,669	 1.93% -2.13% -2.97% 166 SushiSwap SushiSwap SUSHI $328,780,197  $1.42 232,049,314 SUSHI * $251,451,426	 0.23% 7.08% 13.02% 167 API3 API3 API3 $328,391,356  $3.80 86,421,978 API3 * $42,818,590	 2.27% -5.27% -9.81% 168 Decentralized Social Decentralized Social DESO $327,602,787  $36.87 8,884,536 DESO * $2,700,193	 -1.46% -2.88% -6.89% 169 FLOKI FLOKI FLOKI $326,108,439  $0.00003407 9,570,627,187,457 FLOKI * $34,619,701	 2.11% 0.90% 1.50% 170 Theta Fuel Theta Fuel TFUEL $323,476,789  $0.05009 6,458,338,354 TFUEL * $21,571,679	 5.28% 1.29% 11.92% 171 Aragon Aragon ANT $321,984,704  $7.46 43,179,247 ANT * $5,809,482	 0.92% -1.16% 5.74% 172 Chia Chia XCH $319,740,190  $32.06 9,971,895 XCH * $7,254,075	 0.25% -2.05% -3.48% 173 Treasure Treasure MAGIC $319,353,344  $1.23 259,510,758 MAGIC * $73,062,610	 0.97% -6.06% -7.11% 174 Chromia Chromia CHR $318,820,857  $0.4049 787,434,439 CHR * $10,623,994	 2.13% -2.14% -9.04% 175 Echelon Prime Echelon Prime PRIME $315,844,855  $12.02 26,271,698 PRIME * $3,770,245	 0.92% -4.61% 3.04% 176 Galxe Galxe GAL $312,571,496  $2.97 105,305,665 GAL * $32,189,259	 2.56% -2.61% 23.15% 177 EthereumPoW EthereumPoW ETHW $311,936,800  $2.89 107,818,999 ETHW * $12,491,491	 1.13% -1.81% 2.26% 178 Ravencoin Ravencoin RVN $309,870,679  $0.02287 13,549,510,048 RVN	$16,925,677	 1.42% 0.60% 9.12% 179 ssv.network ssv.network SSV $307,303,369  $30.73 10,000,000 SSV * $25,598,458	 1.54% -3.31% -2.09% 180 Decred Decred DCR $307,124,220  $19.35 15,874,397 DCR	$6,591,378	 0.06% 8.32% 12.84% 181 PayPal USD PayPal USD PYUSD $304,755,970  $0.9998 304,826,578 PYUSD * $11,042,168	 <0.01% <0.01% 0.05% 182 UMA UMA UMA $304,530,630  $3.88 78,386,831 UMA * $22,536,058	 2.38% 0.36% -7.57% 183 0x Protocol 0x Protocol ZRX $302,554,752  $0.357 847,496,055 ZRX * $26,456,172	 1.68% -0.40% 5.51% 184 Centrifuge Centrifuge CFG $302,033,652  $0.6384 473,111,796 CFG * $1,747,836	 0.25% 7.45% -4.04% 185 Flux Flux FLUX $300,456,680  $0.8814 340,901,801 FLUX	$18,246,416	 2.27% 1.41% 22.58% 186 JUST JUST JST $299,009,510  $0.03359 8,902,080,000 JST * $41,495,955	 0.41% -3.54% 0.34% 187 Helium Mobile Helium Mobile MOBILE $298,612,655  $0.00363 82,262,267,398 MOBILE * $13,075,694	 1.35% -13.84% -4.81% 188 dogwifhat dogwifhat WIF $295,747,792  $0.2961 998,920,173 WIF * $42,429,154	 3.70% -8.16% -17.56% 189 Tellor Tellor TRB $294,740,114  $115.46 2,552,752 TRB	$50,706,770	 0.99% 1.11% -8.18% 190 Ankr Ankr ANKR $293,673,594  $0.02937 10,000,000,000 ANKR * $22,434,568	 2.52% -3.05% 5.98% 191 Storj Storj STORJ $293,362,039  $0.718 408,580,225 STORJ * $108,342,413	 1.79% -1.06% 8.91% 192 SPACE ID SPACE ID ID $293,029,928  $0.6033 485,731,152 ID * $74,134,515	 0.94% -1.46% 2.78% 193 MX TOKEN MX TOKEN MX $282,013,911  $2.85 98,959,034 MX * $2,611,537	 0.07% 0.76% 0.60% 194 Band Protocol Band Protocol BAND $281,108,080  $2.02 139,300,567 BAND * $8,900,646	 1.42% -0.16% -0.73% 195 Memecoin Memecoin MEME $280,504,779  $0.02676 10,482,959,513 MEME * $83,424,800	 0.36% -4.04% 2.21% 196 AIOZ Network AIOZ Network AIOZ $278,879,017  $0.2594 1,075,006,068 AIOZ * $8,013,859	 3.23% -14.54% 47.13% 197 Kadena Kadena KDA $277,660,097  $1.05 263,736,187 KDA	$10,320,761	 -0.38% -5.09% -8.55% 198 Threshold Threshold T $276,105,983  $0.02879 9,591,895,882 T * $15,657,347	 1.98% -0.86% -3.00% 199 iExec RLC iExec RLC RLC $276,095,067  $3.81 72,382,548 RLC * $62,771,871	 3.39% -7.99% 50.86% 200 TerraClassicUSD TerraClassicUSD USTC '
stocks = collect_crypto_data(symbols)
stocks = remove_duplicates(stocks)


print(len(stocks))
flat_stocks = [item[0] for item in stocks]
start_date = "2012-01-01"
end_date = "2024-01-26"


# Collecting stocks with specified data length then adding date and ticker index names
all_stock_data = pd.DataFrame()
test_stocks = flat_stocks[:1000]
min_data_length = 3035
filtered_stocks = [ticker for ticker in test_stocks if len(yf.download(tickers=ticker, start=start_date, end=end_date)) >= min_data_length]
all_stock_data = yf.download(tickers=filtered_stocks,
                      start=start_date,
                      end=end_date).stack()

all_stock_data.index.names = ['date', 'ticker']
all_stock_data.columns = all_stock_data.columns.str.lower()


#calculating: garman_klass_vol, rsi, bb_low/mid/high, atr, macd and dollar volume
all_stock_data = Calculations(all_stock_data)

#getting technical analysis columns
last_cols = [c for c in all_stock_data.columns.unique(0) if c not in ['dollar_volume', 'volume', 'open',
                                                          'high', 'low', 'close']]

data = (pd.concat([all_stock_data.unstack('ticker')['dollar_volume'].resample('M').mean().stack('ticker').to_frame('dollar_volume'),
                   all_stock_data.unstack()[last_cols].resample('M').last().stack('ticker')],
                  axis=1)).dropna()

#discard low liquidity stocks
data['dollar_volume'] = (data.loc[:, 'dollar_volume'].unstack('ticker').rolling(5*12, min_periods=12).mean().stack())
data['dollar_vol_rank'] = (data.groupby('date')['dollar_volume'].rank(ascending=False))
data = data[data['dollar_vol_rank']<150].drop(['dollar_volume', 'dollar_vol_rank'], axis=1)


def calculate_returns(df):
    outlier_cutoff = 0.005
    lags = [1, 2, 3, 6, 9, 12]

    for lag in lags:
        df[f'return_{lag}m'] = (df['adj close']
                                .pct_change(lag)
                                .pipe(lambda x: x.clip(lower=x.quantile(outlier_cutoff),
                                                       upper=x.quantile(1 - outlier_cutoff)))
                                .add(1)
                                .pow(1 / lag)
                                .sub(1))
    return df


data = data.groupby(level=1, group_keys=False).apply(calculate_returns).dropna()

factor_data = web.DataReader('F-F_Research_Data_5_Factors_2x3',
                               'famafrench',
                               start='2010')[0].drop('RF', axis=1)


factor_data.index = factor_data.index.to_timestamp()
factor_data = factor_data.resample('M').last().div(100)
factor_data.index.name = 'date'
factor_data = factor_data.join(data['return_1m']).sort_index()
observations = factor_data.groupby(level=1).size()
valid_stocks = observations[observations >= 10]
factor_data = factor_data[factor_data.index.get_level_values('ticker').isin(valid_stocks.index)]

betas = (factor_data.groupby(level=1,
                            group_keys=False)
         .apply(lambda x: RollingOLS(endog=x['return_1m'],
                                     exog=sm.add_constant(x.drop('return_1m', axis=1)),
                                     window=min(24, x.shape[0]),
                                     min_nobs=len(x.columns)+1)
         .fit(params_only=True)
         .params
         .drop('const', axis=1)))

factors = ['Mkt-RF', 'SMB', 'HML', 'RMW', 'CMA']

data = (data.join(betas.groupby('ticker').shift()))

data.loc[:, factors] = data.groupby('ticker', group_keys=False)[factors].apply(lambda x: x.fillna(x.mean()))

data = data.drop('adj close', axis=1)

data = data.dropna()

target_rsi_values = [30, 45, 55, 70]

initial_centroids = np.zeros((len(target_rsi_values), 18))

initial_centroids[:, 6] = target_rsi_values
def get_clusters(df):
    df['cluster'] = KMeans(n_clusters=4,
                           random_state=0,
                           init=initial_centroids).fit(df).labels_
    return df

data = data.dropna().groupby('date', group_keys=False).apply(get_clusters)
data = data.drop(['return_12m', 'return_9m', 'return_6m', 'return_3m', 'return_2m'], axis=1)
data.to_csv("crypto_stocks.csv", index=False)
