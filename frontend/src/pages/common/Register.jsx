import React from "react";
import { Button, Form } from "semantic-ui-react";
import { useFormik } from "formik";
import * as Yup from "yup";
import { toast } from "react-toastify";
import { registerApi } from "../../api/user";
import { useNavigate } from "react-router-dom"; // Importa useNavigate

export function Register() {
  const navigate = useNavigate(); // Hook para redirección
  const formik = useFormik({
    initialValues: initialValues(),
    validationSchema: validationSchema(),
    onSubmit: async (formValues) => {
      try {
        const response = await registerApi(formValues);
        const { username } = response;
        navigate("/login"); // Redirige al Dashboard
      } catch (error) {
        toast.error(error.message);
      }
    },
  });
  return (
    <div className="register-admin">
      <div className="register-admin__content">
        <h1>Registro</h1>

        <Form className="register-form-admin" onSubmit={formik.handleSubmit}>
          <label>Username</label>
          <Form.Input
            name="username"
            placeholder="Username"
            value={formik.values.username}
            onChange={(e) => {
              const value = e.target.value.replace(/\s+/g, ""); // Elimina espacios en tiempo real
              formik.setFieldValue("username", value);
            }}
            onBlur={formik.handleBlur}
            error={formik.errors.username}
          />
          <label>Correo electrónico</label>
          <Form.Input
            name="email"
            placeholder="Correo electrónico"
            value={formik.values.email}
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
            error={formik.errors.email}
          />
          <label>Contraseña</label>
          <Form.Input
            name="password"
            type="password"
            placeholder="Contraseña"
            value={formik.values.password}
            onChange={formik.handleChange}
            error={formik.errors.password}
            autoComplete="false"
          />
          <label>Confirmar Contraseña</label>
          <Form.Input
            name="password_confirm"
            type="password"
            placeholder="Confirmar Contraseña"
            value={formik.values.password_confirm}
            onChange={formik.handleChange}
            error={formik.errors.password_confirm}
            autoComplete="false"
          />
          <Button type="submit" content="Iniciar Sesión" primary fluid />
        </Form>
      </div>
    </div>
  );
}

function initialValues() {
  return {
    username: "",
    email: "",
    password: "",
    password_confirm: "",
  };
}

function validationSchema() {
  return Yup.object({
    username: Yup.string()
      .required("El username es obligatorio")
      .matches(/^\S*$/, "El username no debe contener espacios"), // Prohíbe espacios,
    email: Yup.string()
      .email("Correo electrónico no válido")
      .required("El correo electrónico es obligatorio"),
    password: Yup.string()
      .required("La contraseña es obligatoria")
      .min(8, "La contraseña debe tener al menos 8 caracteres")
      .matches(
        /[A-Z]/,
        "La contraseña debe contener al menos una letra mayúscula"
      )
      .matches(/\d/, "La contraseña debe contener al menos un número")
      .matches(
        /[@$!%*?&#]/,
        "La contraseña debe contener al menos un carácter especial (@$!%*?&#)"
      ),
    password_confirm: Yup.string()
      .required("La confirmacion de contraseña es obligatoria")
      .oneOf([Yup.ref("password"), null], "Las contraseñas no coinciden"),
  });
}
