import type { AlertProps } from "../interfaces/AlertProps";

function Alert({ children, onDismiss }: AlertProps) {
  return (
    <div>
      <div
        className="alert alert-warning alert-dismissible fade show"
        role="alert"
      >
        {children}
        <button
          type="button"
          className="btn-close"
          data-bs-dismiss="alert"
          aria-label="Close"
          onClick={onDismiss}
        ></button>
      </div>
    </div>
  );
}

export default Alert;
