samples = [75, 71, 70, 74]

estimate = 68
error_estimate = 2
error_measurem = 4
true_value = 72

def kalman(measurement):
    global error_estimate
    global estimate
    kalman_gain = error_estimate / (error_estimate + error_measurem)    # STEP 1
    estimate = estimate + kalman_gain * (measurement - estimate)        # STEP 2
    error_estimate = (1 - kalman_gain) * error_estimate
    return estimate

for s in samples:
    print(kalman(s))
