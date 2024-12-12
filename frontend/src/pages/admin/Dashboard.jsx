import React from "react";
import { Button } from "semantic-ui-react";
import { useAuth } from "../../hooks/useAuth";

export function Dashboard() {
  const { logout, auth } = useAuth();
  const user = auth.me;

  return (
    <div>
      <h1>Dashboard Page</h1>
      <h3>Bienvenido {user.email}</h3>
      <Button type="submit" content="Cerrar Sesión" onClick={logout} />
    </div>
  );
}
