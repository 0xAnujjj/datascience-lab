"""
Real-Time Airplane Tracking Visualization System for Asia Region

This application demonstrates key Computer Graphics concepts including:
1. Coordinate Transformation (Geographic to Screen)
2. Translation Transformation (Airplane movement)
3. Rotation Transformation (Airplane heading)
4. Scaling Transformation (Zoom functionality)
5. Animation Loop (Frame refresh)
6. Linear Interpolation (Smooth movement)

Author: Academic Lab Project
Date: 2026
"""

import pygame
import requests
import math
import time
from typing import Dict, List, Tuple, Optional
import json

# ============================================================================
# CONSTANTS AND CONFIGURATION
# ============================================================================

# Screen dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

# Asia region bounds (approximate)
ASIA_MIN_LAT = -10.0
ASIA_MAX_LAT = 55.0
ASIA_MIN_LON = 60.0
ASIA_MAX_LON = 150.0

# Colors
COLOR_BACKGROUND = (15, 25, 35)
COLOR_MAP = (30, 50, 70)
COLOR_AIRPLANE_DEFAULT = (255, 200, 0)
COLOR_TEXT = (255, 255, 255)
COLOR_TRAIL = (100, 150, 200)
COLOR_HOVER_BG = (40, 60, 80, 200)

# API Configuration
# Using OpenSky Network API (Free, no API key required)
API_URL = "https://opensky-network.org/api/states/all"
API_UPDATE_INTERVAL = 10  # seconds between API calls

# Animation settings
INTERPOLATION_STEPS = 30  # Steps for smooth movement
FPS = 60

# ============================================================================
# MATHEMATICAL FORMULAS AND TRANSFORMATIONS
# ============================================================================

class CoordinateTransformer:
    """
    Handles coordinate transformation between geographic and screen coordinates.
    
    Mathematical Formula:
    For converting latitude/longitude to screen coordinates:
    
    x_screen = (lon - min_lon) / (max_lon - min_lon) * screen_width
    y_screen = (max_lat - lat) / (max_lat - min_lat) * screen_height
    
    Note: Y is inverted because screen coordinates have origin at top-left
    """
    
    def __init__(self, min_lat: float, max_lat: float, min_lon: float, max_lon: float,
                 screen_width: int, screen_height: int, zoom: float = 1.0, pan_x: float = 0, pan_y: float = 0):
        self.min_lat = min_lat
        self.max_lat = max_lat
        self.min_lon = min_lon
        self.max_lon = max_lon
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.zoom = zoom
        self.pan_x = pan_x
        self.pan_y = pan_y
    
    def geo_to_screen(self, lat: float, lon: float) -> Tuple[int, int]:
        """
        Convert geographic coordinates (latitude, longitude) to screen pixel coordinates.
        
        Applies:
        1. Normalization: Convert geo coords to 0-1 range
        2. Scaling: Multiply by screen dimensions
        3. Translation: Apply zoom and pan
        """
        # Normalize coordinates (0 to 1)
        norm_x = (lon - self.min_lon) / (self.max_lon - self.min_lon)
        norm_y = (self.max_lat - lat) / (self.max_lat - self.min_lat)
        
        # Apply scaling transformation (zoom)
        # Formula: P' = P * scale
        center_x = self.screen_width / 2
        center_y = self.screen_height / 2
        
        x = norm_x * self.screen_width
        y = norm_y * self.screen_height
        
        # Apply zoom around center
        x = center_x + (x - center_x) * self.zoom
        y = center_y + (y - center_y) * self.zoom
        
        # Apply translation (pan)
        # Formula: P' = P + translation_vector
        x += self.pan_x
        y += self.pan_y
        
        return (int(x), int(y))
    
    def is_in_view(self, lat: float, lon: float) -> bool:
        """Check if coordinates are within the Asia region bounds"""
        return (self.min_lat <= lat <= self.max_lat and 
                self.min_lon <= lon <= self.max_lon)


def rotate_point(x: float, y: float, angle_degrees: float) -> Tuple[float, float]:
    """
    Apply 2D rotation transformation to a point.
    
    Mathematical Formula (Rotation Matrix):
    | x' |   | cos(θ)  -sin(θ) |   | x |
    | y' | = | sin(θ)   cos(θ) | * | y |
    
    Where θ is the rotation angle in radians
    """
    angle_rad = math.radians(angle_degrees)
    cos_theta = math.cos(angle_rad)
    sin_theta = math.sin(angle_rad)
    
    # Apply rotation matrix
    x_rotated = x * cos_theta - y * sin_theta
    y_rotated = x * sin_theta + y * cos_theta
    
    return (x_rotated, y_rotated)


def linear_interpolation(start: float, end: float, t: float) -> float:
    """
    Linear interpolation (LERP) between two values.
    
    Mathematical Formula:
    result = start + (end - start) * t
    
    Where:
    - start: initial value
    - end: target value
    - t: interpolation factor (0.0 to 1.0)
    
    Used for smooth animation between position updates
    """
    return start + (end - start) * t


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate approximate distance between two geographic coordinates.
    
    Simplified Euclidean distance (good enough for visualization):
    distance = sqrt((lat2-lat1)² + (lon2-lon1)²)
    """
    return math.sqrt((lat2 - lat1)**2 + (lon2 - lon1)**2)


# ============================================================================
# AIRPLANE DATA MODEL
# ============================================================================

class Airplane:
    """
    Represents an airplane with its current and interpolated positions.
    """
    
    def __init__(self, icao24: str, callsign: str, lat: float, lon: float, 
                 heading: float, altitude: float, velocity: float):
        self.icao24 = icao24
        self.callsign = callsign.strip() if callsign else "Unknown"
        
        # Current real position from API
        self.target_lat = lat
        self.target_lon = lon
        
        # Interpolated display position
        self.display_lat = lat
        self.display_lon = lon
        
        self.heading = heading if heading is not None else 0
        self.altitude = altitude if altitude is not None else 0
        self.velocity = velocity if velocity is not None else 0
        
        # For smooth interpolation
        self.interp_step = 0
        self.prev_lat = lat
        self.prev_lon = lon
        
        # Trail history
        self.trail: List[Tuple[float, float]] = [(lat, lon)]
        self.max_trail_length = 20
        
        # Visual properties
        self.color = COLOR_AIRPLANE_DEFAULT
        self.assign_color_by_callsign()
    
    def assign_color_by_callsign(self):
        """Assign color based on airline code in callsign"""
        # Extract first 3 characters as airline code
        airline_code = self.callsign[:3] if len(self.callsign) >= 3 else "UNK"
        
        # Simple hash-based color assignment
        hash_val = sum(ord(c) for c in airline_code)
        
        # Generate distinct colors
        r = (hash_val * 67) % 200 + 55
        g = (hash_val * 131) % 200 + 55
        b = (hash_val * 197) % 200 + 55
        
        self.color = (r, g, b)
    
    def update_target(self, lat: float, lon: float, heading: float, altitude: float, velocity: float):
        """Update target position when new API data arrives"""
        self.prev_lat = self.display_lat
        self.prev_lon = self.display_lon
        
        self.target_lat = lat
        self.target_lon = lon
        self.heading = heading if heading is not None else self.heading
        self.altitude = altitude if altitude is not None else self.altitude
        self.velocity = velocity if velocity is not None else self.velocity
        
        # Reset interpolation
        self.interp_step = 0
        
        # Add to trail
        self.trail.append((lat, lon))
        if len(self.trail) > self.max_trail_length:
            self.trail.pop(0)
    
    def interpolate(self):
        """
        Apply linear interpolation to smooth movement.
        
        This demonstrates the LERP formula in action.
        """
        if self.interp_step < INTERPOLATION_STEPS:
            t = self.interp_step / INTERPOLATION_STEPS
            
            # Apply linear interpolation formula
            self.display_lat = linear_interpolation(self.prev_lat, self.target_lat, t)
            self.display_lon = linear_interpolation(self.prev_lon, self.target_lon, t)
            
            self.interp_step += 1
        else:
            # Interpolation complete
            self.display_lat = self.target_lat
            self.display_lon = self.target_lon


# ============================================================================
# API DATA FETCHER
# ============================================================================

class AviationAPIFetcher:
    """
    Fetches real-time airplane data from OpenSky Network API.
    
    OpenSky Network provides free access to live airplane tracking data
    without requiring an API key (rate limited).
    """
    
    def __init__(self):
        self.last_fetch_time = 0
        self.cache_data = []
    
    def fetch_airplanes(self) -> List[Dict]:
        """
        Fetch airplane data from API.
        
        Returns list of airplane state vectors with:
        - icao24: unique identifier
        - callsign: flight number
        - origin_country: country
        - longitude, latitude: position
        - baro_altitude: altitude in meters
        - velocity: speed in m/s
        - true_track: heading in degrees
        """
        current_time = time.time()
        
        # Respect API rate limits
        if current_time - self.last_fetch_time < API_UPDATE_INTERVAL:
            return self.cache_data
        
        try:
            # Fetch data from OpenSky Network
            # Documentation: https://openskynetwork.github.io/opensky-api/
            response = requests.get(API_URL, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                self.cache_data = data.get('states', [])
                self.last_fetch_time = current_time
                print(f"Fetched {len(self.cache_data)} aircraft from API")
                return self.cache_data
            else:
                print(f"API Error: {response.status_code}")
                return self.cache_data
                
        except Exception as e:
            print(f"Error fetching data: {e}")
            return self.cache_data
    
    def parse_airplane_data(self, state_vector) -> Optional[Dict]:
        """
        Parse OpenSky state vector into airplane dictionary.
        
        State vector format (indices):
        0: icao24
        1: callsign
        2: origin_country
        5: longitude
        6: latitude
        7: baro_altitude
        9: velocity
        10: true_track (heading)
        """
        try:
            # Check if we have valid position data
            if state_vector[5] is None or state_vector[6] is None:
                return None
            
            lon = state_vector[5]
            lat = state_vector[6]
            
            # Filter for Asia region
            if not (ASIA_MIN_LAT <= lat <= ASIA_MAX_LAT and 
                    ASIA_MIN_LON <= lon <= ASIA_MAX_LON):
                return None
            
            return {
                'icao24': state_vector[0],
                'callsign': state_vector[1] if state_vector[1] else "N/A",
                'country': state_vector[2],
                'longitude': lon,
                'latitude': lat,
                'altitude': state_vector[7],
                'velocity': state_vector[9],
                'heading': state_vector[10]
            }
        except Exception as e:
            return None


# ============================================================================
# PYGAME VISUALIZATION APPLICATION
# ============================================================================

class AirplaneTrackingApp:
    """
    Main application class implementing the visualization system.
    
    Demonstrates:
    - Animation loop with frame-based updates
    - Real-time data integration
    - Interactive user interface
    - Multiple coordinate systems
    """
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Real-Time Airplane Tracking - Asia Region")
        self.clock = pygame.time.Clock()
        
        # Coordinate transformer
        self.transformer = CoordinateTransformer(
            ASIA_MIN_LAT, ASIA_MAX_LAT, ASIA_MIN_LON, ASIA_MAX_LON,
            SCREEN_WIDTH, SCREEN_HEIGHT
        )
        
        # API fetcher
        self.api_fetcher = AviationAPIFetcher()
        
        # Airplane tracking
        self.airplanes: Dict[str, Airplane] = {}
        
        # Create airplane sprite
        self.airplane_sprite = self.create_airplane_sprite()
        
        # UI state
        self.zoom = 1.0
        self.pan_x = 0
        self.pan_y = 0
        self.mouse_pos = (0, 0)
        self.hovered_airplane = None
        
        # Fonts
        self.font_small = pygame.font.SysFont('Arial', 12)
        self.font_medium = pygame.font.SysFont('Arial', 16)
        self.font_large = pygame.font.SysFont('Arial', 20, bold=True)
        
        # Stats
        self.frame_count = 0
        self.last_api_update = 0
        
        self.running = True
    
    def create_airplane_sprite(self) -> pygame.Surface:
        """
        Create a simple airplane sprite as a triangle.
        
        This is a basic geometric representation that can be rotated.
        """
        size = 20
        sprite = pygame.Surface((size, size), pygame.SRCALPHA)
        
        # Draw airplane as triangle pointing up
        points = [
            (size // 2, 2),           # nose
            (size // 2 - 6, size - 2), # left wing
            (size // 2 + 6, size - 2)  # right wing
        ]
        pygame.draw.polygon(sprite, (255, 255, 255), points)
        
        # Add detail
        pygame.draw.line(sprite, (200, 200, 200), (size//2, size//2), (size//2, size-2), 2)
        
        return sprite
    
    def rotate_sprite(self, sprite: pygame.Surface, angle: float) -> pygame.Surface:
        """
        Rotate sprite using Pygame's built-in rotation.
        
        Demonstrates rotation transformation.
        Note: Pygame rotates counter-clockwise, heading is clockwise from north.
        """
        # Adjust angle: heading 0° is north, need to rotate to match
        adjusted_angle = -(angle - 90)  # Convert to screen coordinates
        return pygame.transform.rotate(sprite, adjusted_angle)
    
    def update_airplanes(self):
        """
        Fetch and update airplane data from API.
        
        This method demonstrates real-time data integration.
        """
        raw_data = self.api_fetcher.fetch_airplanes()
        
        current_icao_list = []
        
        for state_vector in raw_data:
            airplane_data = self.api_fetcher.parse_airplane_data(state_vector)
            
            if airplane_data is None:
                continue
            
            icao = airplane_data['icao24']
            current_icao_list.append(icao)
            
            if icao in self.airplanes:
                # Update existing airplane
                self.airplanes[icao].update_target(
                    airplane_data['latitude'],
                    airplane_data['longitude'],
                    airplane_data['heading'],
                    airplane_data['altitude'],
                    airplane_data['velocity']
                )
            else:
                # Create new airplane
                self.airplanes[icao] = Airplane(
                    icao,
                    airplane_data['callsign'],
                    airplane_data['latitude'],
                    airplane_data['longitude'],
                    airplane_data['heading'],
                    airplane_data['altitude'],
                    airplane_data['velocity']
                )
        
        # Remove airplanes that are no longer tracked
        icao_to_remove = [icao for icao in self.airplanes.keys() 
                          if icao not in current_icao_list and 
                          time.time() - self.last_api_update > 60]
        
        for icao in icao_to_remove:
            del self.airplanes[icao]
    
    def draw_background(self):
        """Draw the background map"""
        self.screen.fill(COLOR_BACKGROUND)
        
        # Draw simple grid representing map
        grid_color = (40, 60, 80)
        
        # Vertical lines (longitude)
        for lon in range(int(ASIA_MIN_LON), int(ASIA_MAX_LON), 10):
            x, _ = self.transformer.geo_to_screen(ASIA_MIN_LAT, lon)
            pygame.draw.line(self.screen, grid_color, (x, 0), (x, SCREEN_HEIGHT), 1)
        
        # Horizontal lines (latitude)
        for lat in range(int(ASIA_MIN_LAT), int(ASIA_MAX_LAT), 10):
            _, y = self.transformer.geo_to_screen(lat, ASIA_MIN_LON)
            pygame.draw.line(self.screen, grid_color, (0, y), (SCREEN_WIDTH, y), 1)
    
    def draw_trail(self, airplane: Airplane):
        """
        Draw flight trail showing recent movement history.
        
        Demonstrates translation transformation over time.
        """
        if len(airplane.trail) < 2:
            return
        
        points = []
        for lat, lon in airplane.trail:
            x, y = self.transformer.geo_to_screen(lat, lon)
            if 0 <= x < SCREEN_WIDTH and 0 <= y < SCREEN_HEIGHT:
                points.append((x, y))
        
        if len(points) >= 2:
            pygame.draw.lines(self.screen, COLOR_TRAIL, False, points, 2)
    
    def draw_airplane(self, airplane: Airplane):
        """
        Draw airplane sprite with rotation based on heading.
        
        Demonstrates:
        1. Translation: Moving sprite to correct screen position
        2. Rotation: Rotating sprite based on heading angle
        """
        x, y = self.transformer.geo_to_screen(airplane.display_lat, airplane.display_lon)
        
        # Check if airplane is in view
        if not (0 <= x < SCREEN_WIDTH and 0 <= y < SCREEN_HEIGHT):
            return
        
        # Apply rotation transformation
        rotated_sprite = self.rotate_sprite(self.airplane_sprite, airplane.heading)
        
        # Color the sprite
        colored_sprite = rotated_sprite.copy()
        colored_sprite.fill(airplane.color, special_flags=pygame.BLEND_MULT)
        
        # Get rect for centering
        rect = colored_sprite.get_rect(center=(x, y))
        
        # Draw the airplane (translation transformation applied)
        self.screen.blit(colored_sprite, rect)
        
        # Draw callsign
        text = self.font_small.render(airplane.callsign, True, airplane.color)
        text_rect = text.get_rect(center=(x, y - 15))
        self.screen.blit(text, text_rect)
        
        return (x, y, rect.width, rect.height)
    
    def check_hover(self):
        """Check if mouse is hovering over an airplane"""
        self.hovered_airplane = None
        
        for airplane in self.airplanes.values():
            x, y = self.transformer.geo_to_screen(airplane.display_lat, airplane.display_lon)
            
            # Check if mouse is near airplane
            dist = math.sqrt((self.mouse_pos[0] - x)**2 + (self.mouse_pos[1] - y)**2)
            
            if dist < 20:  # Hover radius
                self.hovered_airplane = airplane
                break
    
    def draw_hover_info(self):
        """
        Display airplane information when hovering.
        
        Shows detailed flight data in a tooltip-style box.
        """
        if self.hovered_airplane is None:
            return
        
        airplane = self.hovered_airplane
        
        # Info text
        info_lines = [
            f"Flight: {airplane.callsign}",
            f"ICAO24: {airplane.icao24}",
            f"Altitude: {int(airplane.altitude) if airplane.altitude else 'N/A'} m",
            f"Speed: {int(airplane.velocity * 3.6) if airplane.velocity else 'N/A'} km/h",
            f"Heading: {int(airplane.heading)}°",
        ]
        
        # Calculate box size
        padding = 10
        line_height = 20
        box_width = 250
        box_height = len(info_lines) * line_height + padding * 2
        
        # Position near mouse
        box_x = self.mouse_pos[0] + 20
        box_y = self.mouse_pos[1] + 20
        
        # Keep box on screen
        if box_x + box_width > SCREEN_WIDTH:
            box_x = self.mouse_pos[0] - box_width - 20
        if box_y + box_height > SCREEN_HEIGHT:
            box_y = self.mouse_pos[1] - box_height - 20
        
        # Draw semi-transparent background
        info_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        pygame.draw.rect(info_surface, COLOR_HOVER_BG, (0, 0, box_width, box_height))
        pygame.draw.rect(info_surface, airplane.color, (0, 0, box_width, box_height), 2)
        
        # Draw text
        for i, line in enumerate(info_lines):
            text = self.font_medium.render(line, True, COLOR_TEXT)
            info_surface.blit(text, (padding, padding + i * line_height))
        
        self.screen.blit(info_surface, (box_x, box_y))
    
    def draw_ui(self):
        """Draw UI elements (stats, controls)"""
        # Title
        title = self.font_large.render("Real-Time Airplane Tracking - Asia Region", True, COLOR_TEXT)
        self.screen.blit(title, (10, 10))
        
        # Stats
        stats_lines = [
            f"Aircraft Tracked: {len(self.airplanes)}",
            f"Zoom: {self.zoom:.2f}x",
            f"FPS: {int(self.clock.get_fps())}",
        ]
        
        y_offset = 50
        for line in stats_lines:
            text = self.font_small.render(line, True, COLOR_TEXT)
            self.screen.blit(text, (10, y_offset))
            y_offset += 20
        
        # Controls
        controls = [
            "Controls:",
            "Mouse Wheel: Zoom",
            "Hover: Show Info",
            "ESC: Exit"
        ]
        
        y_offset = SCREEN_HEIGHT - 100
        for line in controls:
            text = self.font_small.render(line, True, (180, 180, 180))
            self.screen.blit(text, (10, y_offset))
            y_offset += 18
    
    def handle_events(self):
        """Handle user input events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            
            elif event.type == pygame.MOUSEMOTION:
                self.mouse_pos = event.pos
            
            elif event.type == pygame.MOUSEWHEEL:
                # Zoom functionality (scaling transformation)
                zoom_delta = 0.1 if event.y > 0 else -0.1
                self.zoom = max(0.5, min(3.0, self.zoom + zoom_delta))
                
                # Update transformer
                self.transformer.zoom = self.zoom
    
    def run(self):
        """
        Main game loop implementing the animation loop pattern.
        
        Loop structure:
        1. Handle events (user input)
        2. Update state (physics, data)
        3. Render (draw everything)
        4. Maintain frame rate
        
        This is the core of real-time graphics applications.
        """
        print("Starting Airplane Tracking Visualization...")
        print("Fetching initial data from OpenSky Network API...")
        
        # Initial data fetch
        self.update_airplanes()
        self.last_api_update = time.time()
        
        print(f"Found {len(self.airplanes)} aircraft in Asia region")
        print("Starting main loop...")
        
        while self.running:
            # 1. Handle Events
            self.handle_events()
            
            # 2. Update State
            # Update airplane positions with interpolation
            for airplane in self.airplanes.values():
                airplane.interpolate()
            
            # Check for API updates
            current_time = time.time()
            if current_time - self.last_api_update >= API_UPDATE_INTERVAL:
                self.update_airplanes()
                self.last_api_update = current_time
            
            # Check hover state
            self.check_hover()
            
            # 3. Render
            self.draw_background()
            
            # Draw trails and airplanes
            for airplane in self.airplanes.values():
                self.draw_trail(airplane)
                self.draw_airplane(airplane)
            
            # Draw UI
            self.draw_ui()
            self.draw_hover_info()
            
            # Update display
            pygame.display.flip()
            
            # 4. Maintain Frame Rate
            self.clock.tick(FPS)
            self.frame_count += 1
        
        pygame.quit()
        print("Application closed.")


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """
    Main entry point for the application.
    """
    print("="*70)
    print("Real-Time Airplane Tracking Visualization System")
    print("Asia Region")
    print("="*70)
    print()
    print("Computer Graphics Concepts Demonstrated:")
    print("1. Coordinate Transformation (Geographic -> Screen)")
    print("2. Translation Transformation (Airplane Movement)")
    print("3. Rotation Transformation (Heading-based Sprite Rotation)")
    print("4. Scaling Transformation (Zoom Functionality)")
    print("5. Animation Loop (Real-time Frame Updates)")
    print("6. Linear Interpolation (Smooth Movement)")
    print()
    print("Data Source: OpenSky Network API")
    print("https://opensky-network.org")
    print()
    print("="*70)
    print()
    
    try:
        app = AirplaneTrackingApp()
        app.run()
    except Exception as e:
        print(f"Error running application: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
