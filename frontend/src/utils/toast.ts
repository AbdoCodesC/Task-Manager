import { toast, type ToastOptions, Bounce } from "react-toastify";

const options: ToastOptions = {
  position: "top-right",
  autoClose: 3000,
  hideProgressBar: true,
  closeButton: false,
  closeOnClick: false,
  pauseOnHover: false,
  draggable: false,
  theme: "light",
  className: "!w-full",
  style: {
    color: "dodgerblue",
    background: "whitesmoke",
  },
};

export const info = (message: string) => toast(message, options);
export const error = (message: string) => toast(message, options);
export const success = (message: string) => toast(message, options);
