
import matplotlib.pyplot as plt
from numpy import single

# Define constants
tRFM_sb = 4
tRFM_ab = 8
tREFI = 80
tREFI_b = 40
MAX_ITER = 3000 #3000
RAAMMT = 48

def get_avg_delay(N, RFMTH, REFTH, RAAMAX, uniform_pattern, single_bank):
  # variable declaration for single/all bank 
  if single_bank: 
    separation = tREFI_b
    tRFM = tRFM_sb
  else: 
    separation = tREFI
    tRFM = tRFM_ab
  tot_delay = 0
  raa = 0

  curr_clk = 0
  last_clk = 0 
  
  additional_raa = 0
  for iter in range(1, MAX_ITER + 1):
    # every activation window
    skip = True
    for ii in range(N):
      if (skip):
        tot_delay += 1
        raa += 1
        if (uniform_pattern): 
          curr_clk += tREFI // N 
        else: 
          curr_clk += 1
      else:
        additional_raa += 1
        
      # Check RAAMMT requirement 
      if (raa >= RAAMMT): 
        extra_cycles = (separation-(curr_clk-last_clk))
        if (extra_cycles > 0 ): 
          if ((curr_clk + extra_cycles) > iter * tREFI): 
            skip = False 
            tot_delay += iter * tREFI - curr_clk
            curr_clk = iter * tREFI
          else: 
            tot_delay += extra_cycles
            curr_clk += extra_cycles

      # Check that tREFI has passed since last RFM 
      if (skip and (raa > RAAMAX and (curr_clk-last_clk >= separation or last_clk == 0))):
        rfm_delay = tRFM

        if uniform_pattern:
          avg_time_per_access = tREFI / N
          avg_time_between_access = avg_time_per_access - 1
          if avg_time_between_access < rfm_delay:
            rfm_delay -= avg_time_between_access
          else:
            rfm_delay = 0

        tot_delay += rfm_delay
        
        # Update RAA due to RFM 
        raa -= RFMTH
        if (raa < 0):
          raa = 0
        
        # Update Clk
        last_clk = curr_clk
        curr_clk += tRFM - 1
        
      if (curr_clk > iter * tREFI): 
        skip = False 
    
    # abstracting the case when there is not enough time to do RFM right before REF   
    curr_clk = iter * tREFI

    # Update RAA due to REF 
    if raa >= REFTH:
      raa -= REFTH
    else:
      raa = 0

    #print("raa is ", raa, " tot_delay is ", tot_delay, " additional raa is: ", additional_raa)
  
  #print("additional_raa is ", additional_raa)
  #print("final delay before ", tot_delay)
  if (additional_raa !=0):
    #assert(raa == 40)
    if (single_bank): 
      available = REFTH + RFMTH * 2
    else: 
      available = REFTH + RFMTH
    
    tot_delay += (additional_raa // available) * tREFI 
    tot_delay += (additional_raa % available)
      
    # abstracted for now, could be more delay 
    if ((additional_raa % available) > REFTH): 
        tot_delay += tRFM
  
  #print("final delay after ", tot_delay)
  avg_delay_iter = tot_delay / MAX_ITER
  avg_delay_access = avg_delay_iter / N
  print("final result is ", avg_delay_access)
  return avg_delay_access

# Main
RFMTH = 16
REFTH = RFMTH // 2
RAAMAX = 3 * RFMTH - 1

# Lists to store data points
avg_delay_cluster_single_bank = []
avg_delay_uniform_single_bank = []
avg_delay_cluster_multi_bank = []
avg_delay_uniform_multi_bank = []

avg_delay_cluster_single_bank_lazy = []
avg_delay_uniform_single_bank_lazy = []
avg_delay_cluster_multi_bank_lazy = []
avg_delay_uniform_multi_bank_lazy = []


for ii in range(1, 41): # 1, 41
  # EAGER
  # Calculate delays for single bank
  #delay_cluster_sb = get_avg_delay(ii, RFMTH, REFTH, RFMTH, 0, 1)
  #delay_uniform_sb = get_avg_delay(ii, RFMTH, REFTH, RFMTH, 1, 1)

 # Calculate delays for multi-bank
  #delay_cluster_mb = get_avg_delay(ii, RFMTH, REFTH, RFMTH, 0, 0)
  #delay_uniform_mb = get_avg_delay(ii, RFMTH, REFTH, RFMTH, 1, 0)

 # LAZY
 # Calculate delays for single bank
  delay_cluster_sb_lazy = get_avg_delay(ii, RFMTH, REFTH, RAAMAX, 0, 1)
  #delay_uniform_sb_lazy = get_avg_delay(ii, RFMTH, REFTH, RAAMAX, 1, 1)

  # Calculate delays for multi-bank
  print(ii)
  #delay_cluster_mb_lazy = get_avg_delay(ii, RFMTH, REFTH, RAAMAX, 0, 0)
  #delay_uniform_mb_lazy = get_avg_delay(ii, RFMTH, REFTH, RAAMAX, 1, 0)


  # Append to respective lists
  #avg_delay_cluster_single_bank.append(delay_cluster_sb)
  #avg_delay_uniform_single_bank.append(delay_uniform_sb)
  #avg_delay_cluster_multi_bank.append(delay_cluster_mb)
  #avg_delay_uniform_multi_bank.append(delay_uniform_mb)

  #avg_delay_cluster_single_bank_lazy.append(delay_cluster_sb_lazy)
  #avg_delay_uniform_single_bank_lazy.append(delay_uniform_sb_lazy)
  #avg_delay_cluster_multi_bank_lazy.append(delay_cluster_mb_lazy)
  #avg_delay_uniform_multi_bank_lazy.append(delay_uniform_mb_lazy)

  # print("N: {}\t AvgC: {:.2f}\tAvgU: {:.2f}".format(ii, delay_cluster_sb, delay_uniform_sb)) 

# Plotting
#plt.figure(figsize=(10, 6))

#plt.plot(range(1, 41), avg_delay_cluster_single_bank, label="Single Bank - Clustered, Eager", marker='o')
#plt.plot(range(1, 41), avg_delay_uniform_single_bank, label="Single Bank - Uniform, Eager", marker='o')
#plt.plot(range(1, 41), avg_delay_cluster_multi_bank, label="Multi Bank - Clustered, Eager", marker='o')
#plt.plot(range(1, 41), avg_delay_uniform_multi_bank, label="Multi Bank - Uniform, Eager", marker='o')

#plt.plot(range(1, 41), avg_delay_cluster_single_bank_lazy, label="Single Bank - Clustered, Lazy", marker='o')
#plt.plot(range(1, 41), avg_delay_uniform_single_bank_lazy, label="Single Bank - Uniform, Lazy", marker='o')
#plt.plot(range(1, 41), avg_delay_cluster_multi_bank_lazy, label="Multi Bank - Clustered, Lazy", marker='o')
#plt.plot(range(1, 41), avg_delay_uniform_multi_bank_lazy, label="Multi Bank - Uniform, Lazy", marker='o')

#plt.xlabel("Number of ACTs per tREFI")
#plt.ylabel("Average Delay")
#plt.legend()
#plt.grid(True)
#plt.tight_layout()

# Save figure to a file
#plt.savefig("average_delay_plot.png")
#plt.show()
