# Music Recommendation System

A full-stack music recommendation application with AI-powered suggestions based on mood, genre, artist, and melody preferences.

## Features

- **Mood-based Recommendations**: Get playlists based on your current mood (Happy, Sad, Neutral)
- **Genre Filtering**: Discover music by genre (Pop, Rock, Jazz)
- **Artist Discovery**: Browse and get recommendations from your favorite artists
- **Melody Selection**: Choose music based on melody type (Upbeat, Mellow, Energetic, Smooth, Rhythmic)
- **Modern UI**: Beautiful, responsive interface with smooth animations
- **Real-time Recommendations**: Instant playlist generation based on your selections

## Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **MongoDB**: NoSQL database for music data
- **TensorFlow/Keras**: LSTM model for music recommendations
- **Pandas**: Data processing and analysis

### Frontend
- **React.js**: Modern JavaScript library for building user interfaces
- **React Icons**: Beautiful icon library
- **CSS3**: Modern styling with gradients and animations

## Project Structure

```
Music Recommendation/
├── backend/
│   └── dt/
│       ├── main.py              # FastAPI backend with recommendation endpoints
│       ├── model2.py            # LSTM model for music prediction
│       └── music_lstm_model.h5   # Trained model file
├── frontend/
│   └── frontend/
│       ├── src/
│       │   ├── components/
│       │   │   ├── Header.js           # App header
│       │   │   ├── MoodSelector.js     # Mood selection component
│       │   │   ├── GenreFilter.js     # Genre filtering
│       │   │   ├── ArtistSelector.js   # Artist selection
│       │   │   ├── MelodySelector.js   # Melody selection
│       │   │   ├── PlaylistDisplay.js  # Recommendation display
│       │   │   └── PlayerBar.js        # Music player
│       │   ├── App.js                  # Main application
│       │   └── App.css                 # Styling
│       └── package.json
└── README.md
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 14+
- MongoDB Atlas account (or local MongoDB)

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend/dt
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install fastapi uvicorn pymongo pandas tensorflow scikit-learn
   ```

4. **Update MongoDB connection:**
   - Open `main.py`
   - Replace the MongoDB URI with your own connection string
   - Update the database and collection names if needed

5. **Start the backend server:**
   ```bash
   uvicorn main:app --reload --port 8000
   ```

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend/frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm start
   ```

4. **Open your browser:**
   Navigate to `http://localhost:3000`

## API Endpoints

### Base URL: `http://localhost:8000`

- `GET /` - Health check
- `GET /songs` - Get all songs
- `GET /artists` - Get list of artists
- `GET /melodies` - Get melody types
- `GET /recommendations/mood/{mood}` - Get mood-based recommendations
- `GET /recommendations/genre/{genre}` - Get genre-based recommendations
- `GET /recommendations/artist/{artist}` - Get artist-based recommendations
- `GET /recommendations/melody/{melody_type}` - Get melody-based recommendations

## Usage

1. **Select Your Mood**: Choose from Happy, Sad, or Neutral to get mood-based playlists
2. **Choose Genre**: Select Pop, Rock, or Jazz to filter by genre
3. **Discover Artists**: Scroll through available artists and click to get their recommendations
4. **Pick Melody**: Choose from different melody types for personalized suggestions
5. **View Recommendations**: See your personalized playlist with song cards

## Features in Detail

### Mood Selection
- Visual mood cards with emoji icons
- Instant playlist generation
- Color-coded mood themes

### Genre Filtering
- Icon-based genre selection
- Real-time filtering
- Smooth transitions

### Artist Discovery
- Horizontal scrollable artist list
- Dynamic artist loading from database
- Click-to-recommend functionality

### Melody Selection
- Multiple melody types
- Visual melody cards
- Instant recommendation updates

### Playlist Display
- Grid layout for song cards
- Play button interactions
- Like and add-to-playlist buttons
- Responsive design

## Customization

### Adding New Moods
1. Update the `moods` array in `MoodSelector.js`
2. Add corresponding backend logic in `main.py`
3. Update the database with new mood data

### Adding New Genres
1. Update the `genres` array in `GenreFilter.js`
2. Add genre validation in backend endpoints
3. Ensure database has corresponding genre data

### Styling Customization
- Modify `App.css` for global styles
- Update component-specific styles
- Customize color schemes and animations

## Troubleshooting

### Common Issues

1. **Backend not starting:**
   - Check if all dependencies are installed
   - Verify MongoDB connection string
   - Ensure port 8000 is available

2. **Frontend not connecting to backend:**
   - Verify backend is running on port 8000
   - Check CORS settings in backend
   - Ensure API endpoints are accessible

3. **No recommendations showing:**
   - Check if database has data
   - Verify API endpoints are working
   - Check browser console for errors

### Database Setup
- Ensure your MongoDB database has a `songs` collection
- Collection should have documents with fields: `Artist`, `Genre`, `Sentiment_Label`
- Add sample data if needed for testing

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.
