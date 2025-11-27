import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import '../styles/Results.css'

const Results = () => {
  const navigate = useNavigate()
  const [activeTab, setActiveTab] = useState('twin')
  const [results, setResults] = useState(null)
  const [communityFeed, setCommunityFeed] = useState([])
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      const resultsRes = await axios.get('http://localhost:8000/api/results/latest')
      setResults(resultsRes.data)
      
      const feedRes = await axios.get('http://localhost:8000/api/community/feed')
      setCommunityFeed(feedRes.data)
      
      const statsRes = await axios.get('http://localhost:8000/api/community/stats')
      setStats(statsRes.data)
      
      setLoading(false)
    } catch (err) {
      console.error('Error:', err)
      setLoading(false)
    }
  }

  const formatTimeAgo = (timestamp) => {
    const now = new Date()
    const created = new Date(timestamp)
    const diffMs = now - created
    const diffMins = Math.floor(diffMs / 60000)
    const diffHours = Math.floor(diffMs / 3600000)
    const diffDays = Math.floor(diffMs / 86400000)
    
    if (diffMins < 1) return 'Just now'
    if (diffMins < 60) return `${diffMins}m ago`
    if (diffHours < 24) return `${diffHours}h ago`
    return `${diffDays}d ago`
  }

  const getMatchColor = (score) => {
    if (score >= 70) return '#2E7D32'
    if (score >= 50) return '#F57C00'
    return '#757575'
  }

  const getPhotoUrl = (businessId) => {
    // Try to load real photo, fallback to stock
    const photoPath = `/photos/${businessId}.jpg`
    return photoPath
  }

  const getYelpUrl = (businessId) => {
    return `https://www.yelp.com/biz/${businessId}`
  }

  const handleImageError = (e) => {
    // Fallback to stock image if real photo doesn't exist
    e.target.src = 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=400&q=80'
  }

  if (loading || !results) {
    return (
      <div className="results-container">
        <div className="loading-state">
          <div className="spinner"></div>
          <p>Loading your results...</p>
        </div>
      </div>
    )
  }

  const topTwin = results.taste_twins[0]

  return (
    <div className="results-container">
      <div className="results-header">
        <div>
          <h1>Your Restaurant Twin Results</h1>
          <p>Discover restaurants perfectly matched to your taste</p>
        </div>
        <button className="retake-btn" onClick={() => navigate('/')}>
          Retake Quiz
        </button>
      </div>

      <div className="tabs">
        <button 
          className={`tab ${activeTab === 'twin' ? 'active' : ''}`}
          onClick={() => setActiveTab('twin')}
        >
          Your Twin
        </button>
        <button 
          className={`tab ${activeTab === 'friends' ? 'active' : ''}`}
          onClick={() => setActiveTab('friends')}
        >
          Friends
        </button>
      </div>

      {activeTab === 'twin' && (
        <div className="twin-section">
          <div className="twin-profile">
            <div className="twin-avatar">
              <div className="avatar-circle">
                {topTwin.name.charAt(0)}
              </div>
              <span className="match-badge">{Math.round(topTwin.score)}% Match</span>
            </div>
            <div className="twin-info">
              <h2>Meet Your Twin: {topTwin.name}</h2>
              <p>📍 Santa Barbara, CA • {topTwin.review_count} Yelp reviews</p>
            </div>
          </div>

          <div className="twin-loves">
            <h3>👍 What {topTwin.name} Loves</h3>
            <div className="tag-list">
              {topTwin.tags.priorities && topTwin.tags.priorities.map(p => (
                <span key={p} className="tag">{p.replace('_', ' ')}</span>
              ))}
              {topTwin.tags.dining_style && topTwin.tags.dining_style.map(s => (
                <span key={s} className="tag">{s}</span>
              ))}
              {topTwin.tags.cuisine_preferences && topTwin.tags.cuisine_preferences.map(c => (
                <span key={c} className="tag">{c}</span>
              ))}
            </div>
          </div>

          <div className="recommendations-section">
            <h2>Restaurants We Think You'll Love</h2>
            <p>Based on your quiz answers and your twin's preferences</p>

            <div className="restaurants-grid">
              {results.recommendations.slice(0, 6).map((restaurant) => (
                <div key={restaurant.business_id} className="restaurant-card">
                  <div className="restaurant-image">
                    <img 
                      src={getPhotoUrl(restaurant.business_id)}
                      alt={restaurant.name}
                      onError={handleImageError}
                    />
                    <div className="price-badge">$$$</div>
                  </div>
                  
                  <div className="restaurant-info">
                    <h3>
                      <a 
                        href={getYelpUrl(restaurant.business_id)} 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="restaurant-link"
                      >
                        {restaurant.name}
                      </a>
                    </h3>
                    <p className="location">📍 {restaurant.address}</p>
                    
                    <div className="ratings">
                      <div className="rating-item">
                        <span className="stars">⭐ {restaurant.overall_stars.toFixed(1)}</span>
                        <span className="label">Overall</span>
                      </div>
                      <div className="rating-item highlight">
                        <span className="stars">⭐ {restaurant.twin_avg_rating.toFixed(1)}</span>
                        <span className="label">Your twin rated it</span>
                      </div>
                    </div>

                    <div className="endorsement">
                      <strong>Endorsed by:</strong> {restaurant.endorsing_twin_names.join(', ')}
                    </div>

                    {restaurant.sample_reviews && restaurant.sample_reviews[0] && (
                      <div className="review-snippet">
                        "{restaurant.sample_reviews[0].substring(0, 120)}..."
                      </div>
                    )}

                    <a 
                      href={getYelpUrl(restaurant.business_id)} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="view-on-yelp-btn"
                    >
                      View on Yelp →
                    </a>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {activeTab === 'friends' && (
        <div className="friends-section">
          {stats && (
            <div className="stats-banner">
              <div className="stat-item">
                <span className="stat-number">{stats.total_submissions}</span>
                <span className="stat-label">Total Submissions</span>
              </div>
              <div className="stat-item">
                <span className="stat-number">{stats.today_submissions}</span>
                <span className="stat-label">Today</span>
              </div>
              <div className="stat-item">
                <span className="stat-number">{stats.average_match_score}%</span>
                <span className="stat-label">Avg Match Score</span>
              </div>
            </div>
          )}

          <h2>Live Feed</h2>
          <p>See who else just found their restaurant twin!</p>

          <div className="feed-grid">
            {communityFeed.map((submission) => (
              <div key={submission.submission_id} className="feed-card">
                <div className="feed-card-header">
                  <div className="user-avatar">
                    {submission.display_name.charAt(0).toUpperCase()}
                  </div>
                  <div className="user-info">
                    <h4>{submission.display_name}</h4>
                    <p className="location">{submission.city}, {submission.state}</p>
                    <p className="time">{formatTimeAgo(submission.created_at)}</p>
                  </div>
                </div>
                
                <div className="match-info">
                  <div className="match-result">
                    <span className="match-label">Matched with:</span>
                    <span className="twin-name">{submission.top_twin_name}</span>
                  </div>
                  <div 
                    className="match-score"
                    style={{ 
                      backgroundColor: getMatchColor(submission.match_score),
                      color: 'white'
                    }}
                  >
                    {submission.match_score.toFixed(0)}% Match
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default Results
