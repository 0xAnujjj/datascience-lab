# Real-Time Airplane Tracking Visualization System

## 🎯 Project Overview

An interactive real-time airplane tracking visualization system that displays live flight data for the Asia region using Python and Pygame. This project demonstrates key Computer Graphics concepts in an academic lab context.

## 🚀 Features

- **Real-Time Data Integration**: Fetches live airplane data from OpenSky Network API
- **Interactive Map Visualization**: 2D map focused on Asia region (60°E to 150°E, -10°N to 55°N)
- **Aircraft Rendering**: Sprite-based airplane visualization with heading-based rotation
- **Smooth Animation**: Linear interpolation for fluid movement between API updates
- **User Interaction**:
  - Zoom in/out using mouse wheel
  - Hover over airplanes to see detailed flight information
  - Flight trails showing recent movement history
  - Color-coded airplanes based on airline
- **Performance Optimized**: 60 FPS rendering with efficient coordinate transformations

## 📚 Computer Graphics Concepts Demonstrated

### 1. Coordinate Transformation
**Concept**: Converting geographic coordinates (latitude, longitude) to screen pixel coordinates.

**Mathematical Formula**:
```
x_screen = (lon - min_lon) / (max_lon - min_lon) × screen_width
y_screen = (max_lat - lat) / (max_lat - min_lat) × screen_height
```

**Implementation**: The `CoordinateTransformer` class handles this transformation, accounting for:
- Normalization of geographic coordinates to [0, 1] range
- Scaling to screen dimensions
- Y-axis inversion (screen origin is top-left, geographic is bottom-left)

### 2. Translation Transformation
**Concept**: Moving objects in 2D space by adding displacement vectors.

**Mathematical Formula**:
```
P' = P + T

Where:
P = original position (x, y)
T = translation vector (tx, ty)
P' = new position (x + tx, y + ty)
```

**Implementation**: Applied to:
- Airplane sprite positioning on screen
- Pan functionality (shifting the entire view)
- Flight trail visualization

### 3. Rotation Transformation
**Concept**: Rotating objects around a point using rotation matrices.

**Mathematical Formula** (2D Rotation Matrix):
```
| x' |   | cos(θ)  -sin(θ) |   | x |
| y' | = | sin(θ)   cos(θ) | × | y |

Where:
- θ is the rotation angle in radians
- (x, y) is the original point
- (x', y') is the rotated point
```

**Implementation**: 
- Airplane sprites rotate based on heading angle
- `rotate_point()` function demonstrates the rotation matrix
- Pygame's `transform.rotate()` is used for sprite rotation

### 4. Scaling Transformation
**Concept**: Changing the size of objects or the entire view.

**Mathematical Formula**:
```
P' = C + (P - C) × S

Where:
P = original position
C = center point (pivot)
S = scale factor
P' = scaled position
```

**Implementation**: 
- Zoom functionality scales the view around screen center
- Zoom range: 0.5x to 3.0x
- Mouse wheel controls zoom level

### 5. Animation Loop
**Concept**: Real-time graphics rendering using a game loop pattern.

**Loop Structure**:
```
while running:
    1. Handle Events (user input)
    2. Update State (physics, data)
    3. Render (draw everything)
    4. Maintain Frame Rate
```

**Implementation**:
- 60 FPS target frame rate
- Frame-independent updates
- Efficient state management

### 6. Linear Interpolation (LERP)
**Concept**: Smooth transition between two values over time.

**Mathematical Formula**:
```
result = start + (end - start) × t

Where:
- start: initial value
- end: target value
- t: interpolation factor [0, 1]
```

**Implementation**:
- Smooths airplane movement between API updates (every 10 seconds)
- 30 interpolation steps for fluid animation
- Applied to both latitude and longitude independently

## 🔧 Technical Architecture

### Data Flow

```
OpenSky API → API Fetcher → Airplane Objects → Coordinate Transform → Screen Rendering
     ↓                           ↓                      ↓                    ↓
   JSON              Python Dict          Interpolated      Pygame Surface
  States                                   Position
```

### Class Structure

1. **CoordinateTransformer**: Handles geographic to screen coordinate conversion
2. **Airplane**: Represents individual aircraft with interpolation
3. **AviationAPIFetcher**: Manages API communication and data parsing
4. **AirplaneTrackingApp**: Main application with rendering loop

## 📦 Installation

### Prerequisites
- Python 3.7 or higher
- Internet connection for API access

### Setup

1. Install dependencies:
```bash
cd AirplaneTracking
pip install -r requirements.txt
```

2. Run the application:
```bash
python main.py
```

## 🎮 Controls

- **Mouse Wheel**: Zoom in/out
- **Mouse Hover**: Show airplane details
- **ESC**: Exit application

## 🌐 API Information

**Data Source**: OpenSky Network
- **URL**: https://opensky-network.org
- **Endpoint**: `/api/states/all`
- **Authentication**: None required (rate-limited)
- **Update Interval**: 10 seconds
- **Coverage**: Global air traffic

**Data Fields Used**:
- `icao24`: Unique aircraft identifier
- `callsign`: Flight number
- `latitude`, `longitude`: Position
- `baro_altitude`: Altitude in meters
- `velocity`: Speed in m/s
- `true_track`: Heading in degrees

## 📊 Mathematical Formulas Reference

### Distance Calculation (Simplified)
```
distance = √((lat₂ - lat₁)² + (lon₂ - lon₁)²)
```

### Angle Conversion
```
radians = degrees × (π / 180)
degrees = radians × (180 / π)
```

### Velocity Conversion
```
km/h = m/s × 3.6
```

## 🎨 Visual Design

### Color Scheme
- **Background**: Dark blue (#0F1923)
- **Map Grid**: Light blue (#283C46)
- **Aircraft**: Color-coded by airline (hash-based)
- **Trails**: Cyan (#649BC8)
- **Text**: White (#FFFFFF)

### Screen Layout
- **Resolution**: 1200x800 pixels
- **Asia Region Bounds**:
  - Latitude: -10° to 55° N
  - Longitude: 60° to 150° E

## 🔍 Code Structure

```
AirplaneTracking/
├── main.py              # Main application
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

### Main Components

**Constants** (Lines 20-45):
- Screen dimensions
- Geographic bounds
- Colors
- API configuration

**Mathematical Utilities** (Lines 47-120):
- `CoordinateTransformer`: Geo to screen conversion
- `rotate_point()`: 2D rotation
- `linear_interpolation()`: LERP
- `calculate_distance()`: Distance formula

**Data Models** (Lines 122-230):
- `Airplane`: Aircraft representation with interpolation
- Color assignment based on airline

**API Integration** (Lines 232-310):
- `AviationAPIFetcher`: Real-time data fetching
- Rate limiting and caching

**Visualization** (Lines 312-600):
- `AirplaneTrackingApp`: Main application class
- Rendering pipeline
- Event handling
- UI elements

## 📝 Academic Explanation

### Why This Project?

This project is ideal for academic labs because it:

1. **Demonstrates Core CG Concepts**: All fundamental transformations are clearly visible
2. **Real-World Application**: Uses actual live data, making it engaging
3. **Visual Feedback**: Immediate visual response to mathematical operations
4. **Scalable Complexity**: Can be extended with additional features
5. **Well-Documented**: Every graphics concept is explained with formulas

### Learning Outcomes

Students will understand:
- How geographic data is visualized on screen
- Practical application of transformation matrices
- Animation techniques in real-time graphics
- Integration of external APIs with graphics applications
- Event-driven programming patterns

## 🔄 Extension Ideas

1. **Enhanced Features**:
   - 3D visualization with altitude
   - Multiple map styles (satellite, terrain)
   - Filter by airline, altitude, or speed
   - Click to track specific airplane
   - Route prediction

2. **Advanced Graphics**:
   - Bezier curves for smooth trails
   - Particle effects for takeoff/landing
   - Heat map of traffic density
   - Time-based replay functionality

3. **Performance**:
   - Spatial partitioning for large datasets
   - Level of detail (LOD) rendering
   - GPU acceleration

## 📖 References

- **OpenSky Network**: https://opensky-network.org/
- **Pygame Documentation**: https://www.pygame.org/docs/
- **Computer Graphics Principles**: Foley et al., "Computer Graphics: Principles and Practice"

## 🐛 Troubleshooting

### Common Issues

**No airplanes showing**:
- Check internet connection
- API might be rate-limited (wait a minute)
- Ensure you're running during peak flight times

**Low performance**:
- Reduce FPS constant
- Increase API update interval
- Disable trail rendering

**API errors**:
- OpenSky Network might be down
- Check firewall settings
- Try VPN if region-blocked

## 📄 License

This is an academic project for educational purposes.

## 👨‍💻 Development Notes

**Key Design Decisions**:

1. **API Choice**: OpenSky Network chosen for free access without API key
2. **Region Focus**: Asia selected for good air traffic density
3. **Update Rate**: 10-second API interval balances freshness and rate limits
4. **Interpolation**: 30 steps provides smooth motion at 60 FPS
5. **Sprite Design**: Simple geometric shape for clarity and easy rotation

**Performance Considerations**:
- Coordinate transformations cached per frame
- Only visible airplanes rendered
- Trail length limited to 20 points
- Efficient dict-based airplane tracking

## 🎓 For Viva/Demo

**Key Points to Explain**:

1. Show the coordinate transformation formula and trace through an example
2. Demonstrate rotation by hovering over different airplanes
3. Explain interpolation - why movement is smooth despite 10s updates
4. Show zoom functionality and explain scaling transformation
5. Discuss trade-offs in API update frequency vs. smoothness

**Demonstration Flow**:
1. Start application
2. Explain the Asia region bounds
3. Show live airplanes appearing
4. Hover to display information
5. Zoom in/out to show scaling
6. Point out color coding by airline
7. Explain trail visualization
8. Walk through code comments

---

**Created for Academic Lab Project - Computer Graphics & Visualization**
