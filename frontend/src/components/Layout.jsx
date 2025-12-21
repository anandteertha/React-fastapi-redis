import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import './Layout.css'

function Layout({ children }) {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <div className="layout">
      <nav className="navbar">
        <div className="nav-container">
          <Link to="/" className="nav-brand">
            NutriBite
          </Link>
          <div className="nav-links">
            <Link to="/">Dashboard</Link>
            <Link to="/meals">Meals</Link>
            <Link to="/preferences">Preferences</Link>
            <Link to="/reports">Reports</Link>
            <Link to="/recommendations">Recommendations</Link>
            {user && (
              <div className="nav-user">
                <span>{user.username}</span>
                <button onClick={handleLogout} className="logout-btn">
                  Logout
                </button>
              </div>
            )}
          </div>
        </div>
      </nav>
      <main className="main-content">
        {children}
      </main>
    </div>
  )
}

export default Layout

