import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import '../styles/Quiz.css'

const Quiz = () => {
  const navigate = useNavigate()
  const [currentQuestion, setCurrentQuestion] = useState(0)
  const [displayName, setDisplayName] = useState('')
  const [showNameInput, setShowNameInput] = useState(false)
  const [submitting, setSubmitting] = useState(false)
  const [answers, setAnswers] = useState({
    priorities: [],
    dining_style: [],
    meal_timing: [],
    cuisines: [],
    adventure_level: '',
    price_sensitivity: ''
  })

  const questions = [
    {
      id: 'priorities',
      title: 'What matters most to you?',
      subtitle: 'Select up to 2',
      max: 2,
      options: [
        { value: 'food_quality', label: 'Food quality', image: 'https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=400' },
        { value: 'atmosphere', label: 'Atmosphere', image: 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=400' },
        { value: 'service', label: 'Service', image: 'https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=400' },
        { value: 'value', label: 'Value for money', image: 'https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=400' }
      ]
    },
    {
      id: 'dining_style',
      title: 'What kind of dining atmosphere do you prefer?',
      subtitle: 'Select up to 2',
      max: 2,
      options: [
        { value: 'casual', label: 'Casual & relaxed', image: 'https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=400' },
        { value: 'upscale', label: 'Fine dining', image: 'https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=400' },
        { value: 'cozy', label: 'Cozy & intimate', image: 'https://images.unsplash.com/photo-1466978913421-dad2ebd01d17?w=400' },
        { value: 'lively', label: 'Lively & bustling', image: 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=400' }
      ]
    },
    {
      id: 'meal_timing',
      title: 'When do you prefer to eat out?',
      subtitle: 'Select all that apply',
      max: 4,
      options: [
        { value: 'breakfast', label: 'Breakfast', image: 'https://images.unsplash.com/photo-1533089860892-a7c6f0a88666?w=400' },
        { value: 'brunch', label: 'Brunch', image: 'https://images.unsplash.com/photo-1484723091739-30a097e8f929?w=400' },
        { value: 'lunch', label: 'Lunch', image: 'https://images.unsplash.com/photo-1529042410759-befb1204b468?w=400' },
        { value: 'dinner', label: 'Dinner', image: 'https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=400' }
      ]
    },
    {
      id: 'cuisines',
      title: 'Pick your favorite cuisines!',
      subtitle: 'Select up to 4',
      max: 4,
      options: [
        { value: 'mexican', label: 'Mexican', image: 'https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=400' },
        { value: 'italian', label: 'Italian', image: 'https://images.unsplash.com/photo-1595295333158-4742f28fbd85?w=400' },
        { value: 'japanese', label: 'Japanese', image: 'https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=400' },
        { value: 'american', label: 'American', image: 'https://images.unsplash.com/photo-1550547660-d9450f859349?w=400' },
        { value: 'chinese', label: 'Chinese', image: 'https://images.unsplash.com/photo-1525755662778-989d0524087e?w=400' },
        { value: 'thai', label: 'Thai', image: 'https://images.unsplash.com/photo-1559314809-0d155014e29e?w=400' },
        { value: 'indian', label: 'Indian', image: 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=400' },
        { value: 'seafood', label: 'Seafood', image: 'https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=400' },
        { value: 'vietnamese', label: 'Vietnamese', image: 'https://images.unsplash.com/photo-1555126634-323283e090fa?w=400' },
        { value: 'greek', label: 'Greek', image: 'https://images.unsplash.com/photo-1544025162-d76694265947?w=400' },
        { value: 'french', label: 'French', image: 'https://images.unsplash.com/photo-1559339352-11d035aa65de?w=400' },
        { value: 'korean', label: 'Korean', image: 'https://images.unsplash.com/photo-1498654896293-37aacf113fd9?w=400' }
      ]
    },
    {
      id: 'adventure_level',
      title: 'How adventurous are you with food?',
      type: 'single',
      options: [
        { value: 'traditional', label: 'Traditional - stick to familiar favorites', image: 'https://images.unsplash.com/photo-1550547660-d9450f859349?w=400' },
        { value: 'moderate', label: 'Moderate - try new things occasionally', image: 'https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=400' },
        { value: 'adventurous', label: 'Adventurous - love unique experiences', image: 'https://images.unsplash.com/photo-1559314809-0d155014e29e?w=400' },
        { value: 'very_adventurous', label: 'Very adventurous - the weirder the better!', image: 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=400' }
      ]
    },
    {
      id: 'price_sensitivity',
      title: 'What is your typical price range?',
      type: 'single',
      options: [
        { value: 'budget', label: 'Budget - under $15', image: 'https://images.unsplash.com/photo-1561758033-d89a9ad46330?w=400' },
        { value: 'moderate', label: 'Moderate - $15-30', image: 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=400' },
        { value: 'upscale', label: 'Upscale - $30-60', image: 'https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=400' },
        { value: 'fine_dining', label: 'Fine dining - over $60', image: 'https://images.unsplash.com/photo-1559339352-11d035aa65de?w=400' }
      ]
    }
  ]

  const handleSelect = (questionId, value) => {
    const currentQ = questions.find(q => q.id === questionId)
    
    if (currentQ.type === 'single') {
      setAnswers({ ...answers, [questionId]: value })
    } else {
      const current = answers[questionId] || []
      const max = currentQ.max || 2
      
      if (current.includes(value)) {
        setAnswers({ ...answers, [questionId]: current.filter(v => v !== value) })
      } else if (current.length < max) {
        setAnswers({ ...answers, [questionId]: [...current, value] })
      }
    }
  }

  const canProceed = () => {
    const currentQ = questions[currentQuestion]
    if (currentQ.type === 'single') {
      return !!answers[currentQ.id]
    }
    return (answers[currentQ.id] || []).length > 0
  }

  const handleNext = () => {
    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1)
    } else {
      setShowNameInput(true)
    }
  }

  const handleSubmit = async () => {
    if (!displayName.trim()) {
      alert('Please enter your name!')
      return
    }

    if (submitting) return
    setSubmitting(true)

    try {
      await axios.post('http://localhost:8000/api/quiz/submit', {
        display_name: displayName,
        tags: {
          priorities: answers.priorities || [],
          dining_style: answers.dining_style || [],
          meal_timing: answers.meal_timing || [],
          cuisines: answers.cuisines || [],
          adventure_level: answers.adventure_level || 'moderate',
          price_sensitivity: answers.price_sensitivity || 'moderate'
        },
        city: 'Santa Barbara',
        state: 'CA'
      })
      
      await new Promise(resolve => setTimeout(resolve, 1500))
      navigate('/results')
    } catch (error) {
      console.error('Error:', error)
      alert('Error submitting quiz. Please try again.')
      setSubmitting(false)
    }
  }

  if (showNameInput) {
    return (
      <div className="quiz-container">
        <div className="name-input-screen">
          <h1>Almost done! What's your name?</h1>
          <p>We'll use this to show your results in the community feed</p>
          <input
            type="text"
            value={displayName}
            onChange={(e) => setDisplayName(e.target.value)}
            placeholder="Enter your name"
            className="name-input-box"
            autoFocus
          />
          <div className="navigation-buttons">
            <button className="btn-back" onClick={() => setShowNameInput(false)}>
              Back
            </button>
            <button 
              className="btn-submit" 
              onClick={handleSubmit}
              disabled={!displayName.trim() || submitting}
            >
              {submitting ? 'Submitting...' : 'Find My Taste Twins!'}
            </button>
          </div>
        </div>
      </div>
    )
  }

  const currentQ = questions[currentQuestion]
  const progress = ((currentQuestion + 1) / questions.length) * 100

  return (
    <div className="quiz-container">
      <div className="quiz-header">
        <h1>Find Your Taste Twin!</h1>
        <p>Answer {questions.length} questions to discover your dining soulmate</p>
      </div>

      <div className="progress-bar">
        <div className="progress-fill" style={{ width: `${progress}%` }}></div>
      </div>

      <div className="question-container">
        <h2 className="question-title">{currentQ.title}</h2>
        {currentQ.subtitle && <p className="question-subtitle">{currentQ.subtitle}</p>}
        
        <div className={currentQ.options.length > 6 ? 'options-grid-large' : 'options-grid'}>
          {currentQ.options.map(option => {
            const isSelected = currentQ.type === 'single' 
              ? answers[currentQ.id] === option.value
              : (answers[currentQ.id] || []).includes(option.value)
            
            return (
              <div
                key={option.value}
                className={`option-card ${isSelected ? 'selected' : ''}`}
                onClick={() => handleSelect(currentQ.id, option.value)}
              >
                <img src={option.image} alt={option.label} />
                <span className="option-label">{option.label}</span>
              </div>
            )
          })}
        </div>

        <div className="navigation-buttons">
          {currentQuestion > 0 && (
            <button className="btn-back" onClick={() => setCurrentQuestion(currentQuestion - 1)}>
              Back
            </button>
          )}
          <button 
            className="btn-next" 
            onClick={handleNext}
            disabled={!canProceed()}
          >
            {currentQuestion < questions.length - 1 ? 'Next' : 'Continue'}
          </button>
        </div>
      </div>
    </div>
  )
}

export default Quiz
