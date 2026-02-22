from brian2 import *

# 1. Parameters
duration = 500 * ms   # Half-second simulation duration
Kp = 0.8              # P Gain (Synaptic Weight)
error_rate = 50 * Hz  # Sensor error (e.g., drone tilted to the right, generating 50 spikes per second)

# 2. Input (Sensor Error): Convert error into spikes using rate coding
sensor_error = PoissonGroup(1, rates=error_rate)

# 3. P-Controller Neuron: Simple LIF (Leaky Integrate-and-Fire) neuron
# Each incoming signal increases the membrane potential v.
# When v > 1, the neuron fires (motor command) and v is reset to 0.
tau = 10 * ms
eqs = '''
dv/dt = -v / tau : 1 (unless refractory)
'''
p_neuron = NeuronGroup(
    1,
    eqs,
    threshold='v > 1',
    reset='v = 0',
    refractory=2*ms,
    method='exact'
)

# 4. Synapse (Connection): Connect error spikes to the controller neuron
# on_pre='v += Kp' means: for every incoming spike, increase neuron voltage by Kp.
syn_P = Synapses(sensor_error, p_neuron, on_pre='v += Kp')
syn_P.connect()

# 5. Monitors: Record what is happening in the simulation
spike_monitor_in = SpikeMonitor(sensor_error)
spike_monitor_out = SpikeMonitor(p_neuron)
state_monitor = StateMonitor(p_neuron, 'v', record=True)

# Start Simulation
print("Simulation running...")
run(duration)

# 6. Print Results
print(f"Incoming Error Signal (Spike Count): {spike_monitor_in.num_spikes}")
print(f"Generated Motor Command (Spike Count): {spike_monitor_out.num_spikes}")

# Optional: Visualize results using matplotlib
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 4))
plt.plot(state_monitor.t/ms, state_monitor.v[0], label='Neuron Potential (v)')
plt.axhline(1, ls='--', c='r', label='Firing Threshold')
plt.xlabel('Time (ms)')
plt.ylabel('Voltage')
plt.title(f'P-Controller Neuron (Kp = {Kp})')
plt.legend()
plt.show()
