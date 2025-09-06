classdef Vector3D
    properties
        x
        y
        z
    end
    
    methods
        function obj = Vector3D(x, y, z)
            obj.x = x;
            obj.y = y;
            obj.z = z;
        end
        
        function dist = distance(obj, other)
            dist = sqrt((obj.x - other.x)^2 + (obj.y - other.y)^2 + (obj.z - other.z)^2);
        end
        
        function result = plus(obj, other)
            result = Vector3D(obj.x + other.x, obj.y + other.y, obj.z + other.z);
        end
        
        function result = minus(obj, other)
            result = Vector3D(obj.x - other.x, obj.y - other.y, obj.z - other.z);
        end
        
        function result = times(obj, scalar)
            result = Vector3D(obj.x * scalar, obj.y * scalar, obj.z * scalar);
        end
    end
end

classdef Missile
    properties
        position
        velocity
        direction
    end
    
    methods
        function obj = Missile(pos, vel)
            if nargin < 2
                vel = 300;
            end
            obj.position = pos;
            obj.velocity = vel;
            obj.direction = Vector3D(0, 0, 0);
        end
        
        function obj = setTarget(obj, target)
            direction = target - obj.position;
            magnitude = sqrt(direction.x^2 + direction.y^2 + direction.z^2);
            obj.direction = Vector3D(...
                direction.x/magnitude * obj.velocity, ...
                direction.y/magnitude * obj.velocity, ...
                direction.z/magnitude * obj.velocity);
        end
        
        function pos = getPositionAtTime(obj, t)
            pos = Vector3D(...
                obj.position.x + obj.direction.x * t, ...
                obj.position.y + obj.direction.y * t, ...
                obj.position.z + obj.direction.z * t);
        end
    end
end

classdef Drone
    properties
        position
        velocity
        direction
        smokeGrenades
    end
    
    methods
        function obj = Drone(pos)
            obj.position = pos;
            obj.velocity = 0;
            obj.direction = Vector3D(0, 0, 0);
            obj.smokeGrenades = 2;
        end
        
        function obj = setFlightParams(obj, vel, target)
            obj.velocity = vel;
            direction = target - obj.position;
            magnitude = sqrt(direction.x^2 + direction.y^2 + direction.z^2);
            obj.direction = Vector3D(...
                direction.x/magnitude * vel, ...
                direction.y/magnitude * vel, ...
                direction.z/magnitude * vel);
        end
        
        function pos = getPositionAtTime(obj, t)
            pos = Vector3D(...
                obj.position.x + obj.direction.x * t, ...
                obj.position.y + obj.direction.y * t, ...
                obj.position.z);
        end
    end
end

classdef SmokeGrenade
    properties
        releasePosition
        releaseTime
        detonationDelay
        SMOKE_SINK_SPEED = 3
        EFFECTIVE_RADIUS = 10
        EFFECTIVE_DURATION = 20
    end
    
    methods
        function obj = SmokeGrenade(pos, rel_time, det_delay)
            obj.releasePosition = pos;
            obj.releaseTime = rel_time;
            obj.detonationDelay = det_delay;
        end
        
        function pos = getCloudPositionAtTime(obj, t)
            if t < obj.releaseTime + obj.detonationDelay
                pos = [];
                return
            end
            
            timeSinceDetonation = t - (obj.releaseTime + obj.detonationDelay);
            dropDistance = obj.SMOKE_SINK_SPEED * timeSinceDetonation;
            
            pos = Vector3D(...
                obj.releasePosition.x, ...
                obj.releasePosition.y, ...
                obj.releasePosition.z - dropDistance);
        end
    end
end

function [total_time, first_intercept] = calculateInterceptionTime(smoke, missile)
    start_time = smoke.releaseTime + smoke.detonationDelay;
    total_time = 0;
    intercept_times = [];
    
    for t = start_time:0.1:(start_time + smoke.EFFECTIVE_DURATION)
        smoke_pos = smoke.getCloudPositionAtTime(t);
        if isempty(smoke_pos)
            continue;
        end
        
        missile_pos = missile.getPositionAtTime(t);
        distance = smoke_pos.distance(missile_pos);
        
        if distance <= smoke.EFFECTIVE_RADIUS
            total_time = total_time + 0.1;
            intercept_times = [intercept_times t];
        end
    end
    
    if isempty(intercept_times)
        first_intercept = 0;
    else
        first_intercept = intercept_times(1);
    end
end

function grenades = optimizeSmokeDeployment(drone, missile, fake_target)
    missile = missile.setTarget(fake_target);
    best_grenades = [];
    best_total_time = 0;
    
    for velocity = 70:10:140
        drone = drone.setFlightParams(velocity, fake_target);
        
        for release_time = 1.5:0.5:5.0
            for detonation_delay = 2.0:0.5:5.0
                release_pos = drone.getPositionAtTime(release_time);
                smoke = SmokeGrenade(release_pos, release_time, detonation_delay);
                
                [total_time, ~] = calculateInterceptionTime(smoke, missile);
                
                if total_time > best_total_time
                    best_total_time = total_time;
                    best_grenades = {smoke};
                end
            end
        end
    end
    
    grenades = best_grenades;
end

function saveResults(grenades, filename)
    if nargin < 2
        filename = 'result1.xlsx';
    end
    
    data = cell(length(grenades), 8);
    headers = {'编号', '无人机编号', '飞行速度(m/s)', '投放时刻(s)', ...
              '起爆延时(s)', '投放点x坐标(m)', '投放点y坐标(m)', '投放点z坐标(m)'};
    
    for i = 1:length(grenades)
        smoke = grenades{i};
        data(i,:) = {i, 'FY1', 120, smoke.releaseTime, smoke.detonationDelay, ...
                     smoke.releasePosition.x, smoke.releasePosition.y, smoke.releasePosition.z};
    end
    
    T = cell2table(data, 'VariableNames', headers);
    writetable(T, filename);
end

% Main script
function main()
    missile_pos = Vector3D(20000, 0, 2000);
    drone_pos = Vector3D(17800, 0, 1800);
    fake_target = Vector3D(0, 0, 0);
    
    missile = Missile(missile_pos);
    drone = Drone(drone_pos);
    
    % Solve Problem 3
    optimal_grenades = optimizeSmokeDeployment(drone, missile, fake_target);
    
    % Save results
    saveResults(optimal_grenades);
end

main();