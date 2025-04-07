// ProtectedRoute.js
import { Navigate, useLocation } from 'react-router-dom';

function ProtectedRoute({ children }) {
  const auth = localStorage.getItem('authToken');
  let location = useLocation();

  if (!auth) {
    return <Navigate to="/login/civilian" state={{ from: location }} replace />;
  }

  return children;
}

export default ProtectedRoute;

//App.js
import ProtectedRoute from './ProtectedRoute';
//...other imports

<Routes>
    <Route path="/" element={<LoginForm userType="Civilian" />} />
    <Route path="/dashboard/civilian" element={<ProtectedRoute><CivilianDashboard/></ProtectedRoute>}/>
    <Route path="/dashboard/lawyer" element={<ProtectedRoute><LawyerDashboard/></ProtectedRoute>}/>
    <Route path="/dashboard/police" element={<ProtectedRoute><PoliceDashboard/></ProtectedRoute>}/>
    //other routes
</Routes>