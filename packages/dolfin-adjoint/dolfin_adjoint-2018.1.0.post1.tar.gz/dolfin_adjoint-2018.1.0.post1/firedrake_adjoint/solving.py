from fenics_adjoint.solving import SolveLinearSystemBlock, SolveVarFormBlock


def __SolveLinearSystemBlock__init__(self, A, u, b, *args, **kwargs):
    lhs = A.form
    func = u.function
    rhs = b.form
    bcs = A.bcs
    super().__init__(lhs, rhs, func, bcs, kwargs)

    # Set up parameters initialization
    self.ident_zeros_tol = A.ident_zeros_tol if hasattr(A, "ident_zeros_tol") else None
    self.assemble_system = A.assemble_system if hasattr(A, "assemble_system") else False

    self.forward_args = args
    if len(self.adj_args) <= 0:
        self.adj_args = self.forward_args


SolveLinearSystemBlock.__init__ = __SolveLinearSystemBlock__init__


def __SolveVarFormBlock__init__(self, equation, func, bcs=[], *args, **kwargs):
    lhs = equation.lhs
    rhs = equation.rhs
    super().__init__(lhs, rhs, func, bcs, kwargs)

    self.forward_args = args
    self.forward_kwargs = kwargs

    if "solver_parameters" in self.forward_kwargs and "mat_type" in self.forward_kwargs["solver_parameters"]:
        self.assemble_kwargs["mat_type"] = self.forward_kwargs["solver_parameters"]["mat_type"]

    if len(self.adj_args) <= 0:
        # self.adj_args = tuple(self.forward_kwargs.get("solver_parameters", {}).values())
        self.adj_kwargs = self.forward_kwargs


SolveVarFormBlock.__init__ = __SolveVarFormBlock__init__



