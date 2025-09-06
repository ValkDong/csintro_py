import numpy as np
import pandas as pd
from typing import Tuple, List
import math

class Vector3D:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z
    
    def __add__(self, other):
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, scalar: float):
        return Vector3D(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def distance_to(self, other) -> float:
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2 + (self.z - other.z)**2)

class Missile:
    def __init__(self, position: Vector3D, velocity: float = 300):
        self.position = position
        self.velocity = velocity  # m/s
        self.direction = Vector3D(0, 0, 0)  # Will be set when target is known
        
    def set_target(self, target: Vector3D):
        direction = target - self.position
        magnitude = math.sqrt(direction.x**2 + direction.y**2 + direction.z**2)
        self.direction = Vector3D(
            direction.x/magnitude * self.velocity,
            direction.y/magnitude * self.velocity,
            direction.z/magnitude * self.velocity
        )
    
    def position_at_time(self, t: float) -> Vector3D:
        return Vector3D(
            self.position.x + self.direction.x * t,
            self.position.y + self.direction.y * t,
            self.position.z + self.direction.z * t
        )

class Drone:
    def __init__(self, position: Vector3D):
        self.position = position
        self.velocity = 0
        self.direction = Vector3D(0, 0, 0)
        self.smoke_grenades = 2
    
    def set_flight_params(self, velocity: float, target: Vector3D):
        self.velocity = velocity
        direction = target - self.position
        magnitude = math.sqrt(direction.x**2 + direction.y**2 + direction.z**2)
        self.direction = Vector3D(
            direction.x/magnitude * velocity,
            direction.y/magnitude * velocity,
            direction.z/magnitude * velocity
        )
    
    def position_at_time(self, t: float) -> Vector3D:
        return Vector3D(
            self.position.x + self.direction.x * t,
            self.position.y + self.direction.y * t,
            self.position.z
        )

class SmokeGrenade:
    def __init__(self, release_position: Vector3D, release_time: float, detonation_delay: float):
        self.release_position = release_position
        self.release_time = release_time
        self.detonation_delay = detonation_delay
        self.SMOKE_SINK_SPEED = 3  # m/s
        self.EFFECTIVE_RADIUS = 10  # m
        self.EFFECTIVE_DURATION = 20  # s
        
    def cloud_position_at_time(self, t: float) -> Vector3D:
        if t < self.release_time + self.detonation_delay:
            return None
        
        time_since_detonation = t - (self.release_time + self.detonation_delay)
        drop_distance = self.SMOKE_SINK_SPEED * time_since_detonation
        
        return Vector3D(
            self.release_position.x,
            self.release_position.y,
            self.release_position.z - drop_distance
        )

def calculate_interception_time(smoke: SmokeGrenade, missile: Missile) -> Tuple[float, float]:
    """Calculate the time period during which the smoke effectively blocks the missile."""
    start_time = smoke.release_time + smoke.detonation_delay
    total_effective_time = 0
    interception_times = []
    
    # Check every 0.1 second interval
    for t in np.arange(start_time, start_time + smoke.EFFECTIVE_DURATION, 0.1):
        smoke_pos = smoke.cloud_position_at_time(t)
        if smoke_pos is None:
            continue
        
        missile_pos = missile.position_at_time(t)
        distance = smoke_pos.distance_to(missile_pos)
        
        if distance <= smoke.EFFECTIVE_RADIUS:
            total_effective_time += 0.1
            interception_times.append(t)
    
    if not interception_times:
        return 0, 0
    
    return total_effective_time, interception_times[0]

def optimize_smoke_deployment(drone: Drone, missile: Missile, fake_target: Vector3D) -> List[SmokeGrenade]:
    """Optimize the deployment of smoke grenades for maximum interception time."""
    missile.set_target(fake_target)
    best_grenades = []
    best_total_time = 0
    
    # Grid search for optimal parameters
    for velocity in np.arange(70, 141, 10):  # Drone velocity
        drone.set_flight_params(velocity, fake_target)
        
        for release_time in np.arange(1.5, 5.0, 0.5):  # Release time
            for detonation_delay in np.arange(2.0, 5.0, 0.5):  # Detonation delay
                release_pos = drone.position_at_time(release_time)
                smoke = SmokeGrenade(release_pos, release_time, detonation_delay)
                
                total_time, _ = calculate_interception_time(smoke, missile)
                
                if total_time > best_total_time:
                    best_total_time = total_time
                    best_grenades = [smoke]
    
    return best_grenades

def save_results(grenades: List[SmokeGrenade], filename: str = 'result1.xlsx'):
    """Save the results to an Excel file."""
    data = []
    for i, grenade in enumerate(grenades, 1):
        data.append({
            '编号': i,
            '无人机编号': 'FY1',
            '飞行速度(m/s)': 120,
            '投放时刻(s)': grenade.release_time,
            '起爆延时(s)': grenade.detonation_delay,
            '投放点x坐标(m)': grenade.release_position.x,
            '投放点y坐标(m)': grenade.release_position.y,
            '投放点z坐标(m)': grenade.release_position.z
        })
    
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)

def main():
    # Initialize problem components
    missile_pos = Vector3D(20000, 0, 2000)
    drone_pos = Vector3D(17800, 0, 1800)
    fake_target = Vector3D(0, 0, 0)
    
    missile = Missile(missile_pos)
    drone = Drone(drone_pos)
    
    # Solve Problem 3
    optimal_grenades = optimize_smoke_deployment(drone, missile, fake_target)
    
    # Save results
    save_results(optimal_grenades)

if __name__ == "__main__":
    main()