import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Quiz from './pages/Quiz'
import Results from './pages/Results'
import './App.css'

function App() {
  console.log('App component rendering')
  
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Quiz />} />
        <Route path="/results" element={<Results />} />
      </Routes>
    </Router>
  )
}

export default App
