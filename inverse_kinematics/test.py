import tinyik
import numpy as np

arm = tinyik.Actuator(['y', [0., -0.01, 0.], 'x', [0., -0.15, 0.], 'x', [0., -0.15, 0.]])
#arm.angles = [np.pi / 6, np.pi / 3]  # or np.deg2rad([30, 60])
arm.ee = [0.5, 0., 0.2]
arm_deg=np.round(np.rad2deg(arm.angles))

print (arm.angles)
print (arm_deg)
print (arm.ee)
