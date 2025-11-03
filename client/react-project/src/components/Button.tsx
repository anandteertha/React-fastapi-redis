import type { ButtonProps } from "../interfaces/ButtonProps";

function Button({ color = "primary", children, onClick }: ButtonProps) {
  return (
    <button className={"btn btn-" + color} onClick={onClick}>
      {children}
    </button>
  );
}

export default Button;
