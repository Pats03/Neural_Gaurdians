import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
// import Home from './pages/Home';
import UserLogin from './Pages/UserLogin'
import PortfolioDashboard from './Pages/ProtfolioDashboard';
import Transaction from './Pages/Transaction';
import Home from './Pages/Home';
import UserSignup from './Pages/UserSignup';
import AdminLogin from './Pages/AdminLogin';
import AdminSignup from './Pages/AdminSignup';
import AdminDashboard from './Pages/AdminDashboard';
import Stats from './Pages/Stats';
// import UserSettings from './pages/user/UserSettings';
// import AdminDashboard from './pages/admin/AdminDashboard';
// import AdminReports from './pages/admin/AdminReports';
// import NotFound from './pages/NotFound';

function App() {
  return (
    <Router>
      <Routes>
        {/* Home Page */}
        {/* <Route path="/" element={<Home />} /> */}

        {/* User Routes */}
        <Route path="/" element={<Home />} />
        <Route path="/userlogin" element={<UserLogin />} />
        <Route path="/usersignup" element={<UserSignup />} />
        <Route path="userdashboard" element={<PortfolioDashboard />} />
        <Route path="transaction" element={<Transaction />} />

        <Route path="/adminlogin" element={<AdminLogin />} />
        <Route path="/adminsignup" element={<AdminSignup />} />
        <Route path="/admindashboard" element={<AdminDashboard />} />
        <Route path="/stats" element={<Stats />} />
        {/* Admin Routes */}
        {/* <Route path="/admin" element={<AdminDashboard />}> */}
        {/* <Route path="reports" element={<AdminReports />} /> */}
        {/* </Route> */}

        {/* 404 */}
        {/* <Route path="*" element={<NotFound />} /> */}
      </Routes>
    </Router>
  );
}

export default App;
