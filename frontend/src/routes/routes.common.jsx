import { CommonLayout } from "../layouts/CommonLayout";
import { Login, Register, ErrorNoPage} from "../pages/common";

const routesCommon = [
  {
    path: "/login",
    layout: CommonLayout,
    component: Login,
  },
  {
    path: "/register",
    layout: CommonLayout,
    component: Register,
  },
  {
    path: "*",
    layout: CommonLayout,
    component: ErrorNoPage,
  },
];

export default routesCommon;
