"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_alg.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow


#  You MUST provide the following two functions
#  with these signatures. You must keep
#  these signatures even if you don't use all the
#  same arguments.
#

speedDict = { 0: (15, 34), 1: (15, 32), 2: (15, 30), 3: (11.428, 28), 4: (13.333, 26)}

distanceDict = [200, 200, 200, 400]

maxLookup = { 200: (13, 30), 300: (20, 0), 400: (27, 0), 600: (40, 0), 1000: (75, 0), 1200: (90, 0), 1400: (116, 40)}

def open_time(control_dist_km, brevet_dist_km, brevet_start_time: arrow):
    """
    Args:
       control_dist_km:  number, control distance in kilometers
       brevet_dist_km: number, nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  An arrow object
    Returns:
       An arrow object indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """
    if (control_dist_km <= 0):
        return brevet_start_time
    
    if (control_dist_km > brevet_dist_km):
        control_dist_km = brevet_dist_km

    minutes = 0

    for x in range(4):
        if control_dist_km >= distanceDict[x]:
            minutes += (distanceDict[x] / speedDict[x][1]) * 60
            control_dist_km -= distanceDict[x]
        elif control_dist_km <= 0:
            break
        else:
            minutes += (control_dist_km / speedDict[x][1]) * 60
            break


    minutes = round(minutes)
    return brevet_start_time.shift(minutes=+minutes)


def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, control distance in kilometers
          brevet_dist_km: number, nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  An arrow object
    Returns:
       An arrow object indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """
    if (control_dist_km <= 0):
        return brevet_start_time.shift(hours=+1)    

    if (control_dist_km <= 60):
        minutes = round((control_dist_km / (20 / 60)) + 60)
        return brevet_start_time.shift( minutes=+minutes )

    if (control_dist_km >= (brevet_dist_km)):
        return brevet_start_time.shift(hours=+maxLookup[brevet_dist_km][0], minutes=+maxLookup[brevet_dist_km][1])

    minutes = 0

    for x in range(4):
        if control_dist_km >= distanceDict[x]:
            minutes += (distanceDict[x] / speedDict[x][0]) * 60
            control_dist_km -= distanceDict[x]
        elif control_dist_km <= 0:
            break
        else:
            minutes += (control_dist_km / speedDict[x][0]) * 60
            break

    minutes = round(minutes)
    return brevet_start_time.shift(minutes=+minutes)