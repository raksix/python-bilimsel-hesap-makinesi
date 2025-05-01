import customtkinter as ctk
import math
# Use sympy for safer evaluation and advanced math
import sympy
# Import necessary sympy functions and types
from sympy import (sympify, N, pi, E, sqrt, log, ln, sin as sympy_sin, cos as sympy_cos, tan as sympy_tan, # Renamed base trig
                   asin as sympy_asin, acos as sympy_acos, atan as sympy_atan, # Renamed base inverse trig
                   symbols, Number, diff, integrate, solve, Symbol, Pow, Abs, root, exp, Eq, # Added Eq
                   init_printing, Function, Expr, zoo) # Added zoo
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
import numpy as np # Import NumPy for matrix operations
from tokenize import TokenError # Import TokenError for explicit handling

# For better printing of sympy results if needed (optional)
init_printing(use_unicode=True)

# ==============================================================================
# Custom SymPy Functions for Angle Mode Awareness
# ==============================================================================
# We need a way for these functions to know the current angle_mode.
# We can pass the CalculatorApp instance or the mode itself during evaluation.
# Let's try passing the mode to a custom evaluation method later.

class angle_aware_sin(Function):
    @classmethod
    def eval(cls, arg, angle_mode='DEG'): # Default mode for symbolic eval if needed
        # Symbolic evaluation if possible
        if arg == 0: return sympy.Integer(0)
        # Add other symbolic simplifications if desired
        return None # Return None if no symbolic evaluation

    def _eval_evalf(self, prec, angle_mode='DEG'):
        # Numerical evaluation using N() or evalf()
        arg_val = self.args[0].evalf(prec)
        if angle_mode == 'DEG':
            return sympy_sin(arg_val * pi / 180).evalf(prec)
        else: # RAD
            return sympy_sin(arg_val).evalf(prec)

class angle_aware_cos(Function):
    @classmethod
    def eval(cls, arg, angle_mode='DEG'):
        if arg == 0: return sympy.Integer(1)
        return None
    def _eval_evalf(self, prec, angle_mode='DEG'):
        arg_val = self.args[0].evalf(prec)
        if angle_mode == 'DEG':
            return sympy_cos(arg_val * pi / 180).evalf(prec)
        else:
            return sympy_cos(arg_val).evalf(prec)

class angle_aware_tan(Function):
    @classmethod
    def eval(cls, arg, angle_mode='DEG'):
        if arg == 0: return sympy.Integer(0)
        return None
    def _eval_evalf(self, prec, angle_mode='DEG'):
        arg_val = self.args[0].evalf(prec)
        # Handle potential pole errors for tan(90), tan(270) etc.
        if angle_mode == 'DEG':
            # Check for multiples of 90 degrees (excluding 180, 360...)
            if (arg_val % 180) == 90:
                 raise sympy.PoleError("tan argument is multiple of 90 degrees") # Or return zoo?
            return sympy_tan(arg_val * pi / 180).evalf(prec)
        else:
             # Check for multiples of pi/2
            if (arg_val / (pi/2)) % 2 == 1:
                 raise sympy.PoleError("tan argument is multiple of pi/2")
            return sympy_tan(arg_val).evalf(prec)

# Similar classes for asin, acos, atan, returning degrees if mode is DEG
class angle_aware_asin(Function):
    @classmethod
    def eval(cls, arg, angle_mode='DEG'): return None
    def _eval_evalf(self, prec, angle_mode='DEG'):
        arg_val = self.args[0].evalf(prec)
        rad_result = sympy_asin(arg_val).evalf(prec)
        if angle_mode == 'DEG':
            return (rad_result * 180 / pi).evalf(prec)
        else:
            return rad_result

class angle_aware_acos(Function):
    @classmethod
    def eval(cls, arg, angle_mode='DEG'): return None
    def _eval_evalf(self, prec, angle_mode='DEG'):
        arg_val = self.args[0].evalf(prec)
        rad_result = sympy_acos(arg_val).evalf(prec)
        if angle_mode == 'DEG':
            return (rad_result * 180 / pi).evalf(prec)
        else:
            return rad_result

class angle_aware_atan(Function):
    @classmethod
    def eval(cls, arg, angle_mode='DEG'): return None
    def _eval_evalf(self, prec, angle_mode='DEG'):
        arg_val = self.args[0].evalf(prec)
        rad_result = sympy_atan(arg_val).evalf(prec)
        if angle_mode == 'DEG':
            return (rad_result * 180 / pi).evalf(prec)
        else:
            return rad_result

# Custom functions for log10, root_3, pow10
class custom_log10(Function):
    @classmethod
    def eval(cls, arg): return None
    def _eval_evalf(self, prec):
        arg_val = self.args[0].evalf(prec)
        return log(arg_val, 10).evalf(prec)

class custom_root3(Function):
    @classmethod
    def eval(cls, arg): return None
    def _eval_evalf(self, prec):
        arg_val = self.args[0].evalf(prec)
        return root(arg_val, 3).evalf(prec)

class custom_pow10(Function):
    @classmethod
    def eval(cls, arg): return None
    def _eval_evalf(self, prec):
        arg_val = self.args[0].evalf(prec)
        return Pow(10, arg_val).evalf(prec)


# ==============================================================================
# Main Application Class
# ==============================================================================
class CalculatorApp(ctk.CTk):
    # ==============================================================================
    # Initialization and UI Setup
    # ==============================================================================
    def __init__(self):
        """Initializes the calculator application, sets up UI and state."""
        super().__init__()

        # --- Window Configuration ---
        self.title("Bilimsel Hesap Makinesi (FX-99ICW Klonu)")
        self.geometry("480x720") # Adjust size as needed

        # --- State Variables ---
        self.angle_mode = "DEG" # Default angle mode: DEG or RAD
        self.shift_active = False # Track SHIFT state
        self.insert_mode = False # Track INS state (Placeholder)
        self.last_result = 0 # Store the last calculated result for Ans
        self.variables = { # Dictionary to store variable values
            'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0,
            'Ans': 0, 'x': 0, 'y': 0 # Added 'y'
        }
        # Define sympy symbols for variables and symbolic calculations
        self.sympy_vars = symbols('A B C D E F Ans x y') # Added 'y'

        # --- Button Shift Mappings ---
        # Maps primary text to secondary (shifted) text/function representation
        self.shift_map = {
            'sin': 'asin', 'cos': 'acos', 'tan': 'atan',
            'log': '10^',  # Represents 10**x
            'ln': 'e^',    # Represents E**x or exp(x)
            '√': '³√',     # Cube root
            'x²': 'x³',     # Cube
            # Add other mappings as needed
        }
        # Store the inverse map for toggling back (maps shifted text to primary text)
        self.inverse_shift_map = {v: k for k, v in self.shift_map.items()}

        # --- GUI Elements ---
        # Create the display and button sections
        self._create_display()
        self._create_buttons()

        # --- Initial State Update ---
        self.update_mode_label() # Set initial mode label text

    def _create_display(self):
        """Creates the display area (mode label and text box)."""
        self.display_frame = ctk.CTkFrame(self)
        self.display_frame.pack(pady=10, padx=10, fill="x")

        # Mod Göstergeleri
        self.mode_label = ctk.CTkLabel(self.display_frame, text="", anchor="w") # Text set by update_mode_label
        self.mode_label.pack(fill="x")

        # Ana Ekran (Çok satırlı giriş/çıkış için)
        self.display = ctk.CTkTextbox(self.display_frame, height=100, font=("Arial", 20))
        self.display.pack(fill="both", expand=True)
        self.display.insert("0.0", "0") # Başlangıç değeri
        self.display.configure(state="disabled") # Başlangıçta düzenlenemez

    def _create_buttons(self):
        """Creates the button grid layout."""
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Button layout definition - Added '=' next to EXE
        self.button_definitions = [
            # Row 0: Function Keys (Top)
            ('SHIFT', 0, 0), ('d/dx', 0, 1), ('∫dx', 0, 2), ('solve', 0, 3), ('TOOLS', 0, 4), ('SETTINGS', 0, 5),
            # Row 1: Navigation / Mode / Parentheses
            ('(', 1, 0), (')', 1, 1), ('HOME', 1, 2), ('↑', 1, 3), ('FORMAT', 1, 4), ('ON', 1, 5),
            # Row 2: Navigation / Functions / Variables
            ('x', 2, 0), ('y', 2, 1), ('←', 2, 2), ('OK', 2, 3), ('→', 2, 4), ('INS', 2, 5),
            # Row 3: Functions / Navigation
            ('√', 3, 0), ('log', 3, 1), ('x²', 3, 2), ('↓', 3, 3), ('ln', 3, 4), ('(-)', 3, 5), # Moved x² here
            # Row 4: Numbers & Basic Ops
            ('7', 4, 0), ('8', 4, 1), ('9', 4, 2), ('DEL', 4, 3, 1, 2), ('AC', 4, 5),
            # Row 5: Numbers & Basic Ops
            ('4', 5, 0), ('5', 5, 1), ('6', 5, 2), ('×', 5, 3), ('÷', 5, 4),
            # Row 6: Numbers & Basic Ops
            ('1', 6, 0), ('2', 6, 1), ('3', 6, 2), ('+', 6, 3), ('-', 6, 4),
            # Row 7: Numbers, Constants, Execute
            ('0', 7, 0), ('.', 7, 1), ('x10^', 7, 2), ('Ans', 7, 3), ('EXE', 7, 4), ('=', 7, 5), # Added '=' button
            # Row 8: Other Functions / Constants
            ('sin', 8, 0), ('cos', 8, 1), ('tan', 8, 2), ('π', 8, 3), ('e', 8, 4), ('QR', 8, 5), # 'e' button is here
            # Row 9: Variable Keys
            ('A', 9, 0), ('B', 9, 1), ('C', 9, 2), ('D', 9, 3), ('E', 9, 4), ('F', 9, 5),
        ]

        # Grid configuration
        rows, cols = 10, 6
        for i in range(rows):
            self.button_frame.grid_rowconfigure(i, weight=1)
        for i in range(cols):
            self.button_frame.grid_columnconfigure(i, weight=1)

        # Button creation and placement
        self.buttons = {} # Store button widgets {primary_text: widget}
        for button_data in self.button_definitions:
            primary_text = button_data[0]
            row, col = button_data[1], button_data[2]
            rowspan = button_data[3] if len(button_data) > 3 else 1
            colspan = button_data[4] if len(button_data) > 4 else 1

            action = lambda p_text=primary_text: self.on_button_press(p_text)
            button = ctk.CTkButton(self.button_frame, text=primary_text, command=action, font=("Arial", 12))

            # Special styling for some keys (optional)
            if primary_text in ['AC', 'DEL']:
                 button.configure(fg_color=("gray70", "gray30")) # Different color for clear/delete
            elif primary_text == 'EXE': # Only EXE gets blue color now
                 button.configure(fg_color="blue") # Emphasize EXE
            elif primary_text == 'SHIFT':
                 button.configure(fg_color="orange") # Emphasize SHIFT
            # Removed the styling for '=' button

            button.grid(row=row, column=col, rowspan=rowspan, columnspan=colspan, padx=1, pady=1, sticky="nsew")
            self.buttons[primary_text] = button

    # ==============================================================================
    # UI Update and State Management Methods
    # ==============================================================================
    def update_mode_label(self):
        """Updates the mode label text (angle, shift, insert indicators)."""
        shift_indicator = "[S]" if self.shift_active else ""
        insert_indicator = "[INS]" if self.insert_mode else "" # Placeholder indicator
        # Add other modes later (COMP, STAT, etc.)
        self.mode_label.configure(text=f"MODE: COMP | {self.angle_mode} {shift_indicator} {insert_indicator}")

    def toggle_shift(self):
        """Toggles the SHIFT state, updates button texts, and UI indicators."""
        self.shift_active = not self.shift_active
        self.update_mode_label()

        # Update button texts based on shift state
        for primary_text, button in self.buttons.items():
            current_button_text = button.cget("text")
            target_text = primary_text # Default to primary text

            if self.shift_active:
                # Get shifted text if mapping exists
                shifted_text = self.shift_map.get(primary_text)
                if shifted_text:
                    target_text = shifted_text
                # Special handling for variable keys A-F for STO indication
                elif primary_text in ['A', 'B', 'C', 'D', 'E', 'F']:
                     target_text = f"STO {primary_text}"
            else:
                # Revert to primary text
                # Check if the current text is a shifted value that needs reverting
                original_text_lookup = self.inverse_shift_map.get(current_button_text)
                if original_text_lookup:
                    target_text = original_text_lookup # Revert using inverse map
                # Revert variable keys A-F if they show STO
                elif current_button_text.startswith("STO ") and primary_text in ['A', 'B', 'C', 'D', 'E', 'F']:
                     target_text = primary_text

            # Update button text only if it needs changing
            if current_button_text != target_text:
                button.configure(text=target_text)

        # Update SHIFT button appearance
        shift_button_color = "red" if self.shift_active else "orange"
        self.buttons['SHIFT'].configure(fg_color=shift_button_color)

    def toggle_insert_mode(self):
        """Toggles the Insert mode state."""
        self.insert_mode = not self.insert_mode
        self.update_mode_label()
        print(f"Insert mode: {'Active' if self.insert_mode else 'Inactive'}")

    # ==============================================================================
    # Event Handling (Button Presses)
    # ==============================================================================
    def on_button_press(self, primary_char):
        """Handles all button press events based on primary button identity."""

        # --- Determine actual character/function based on SHIFT state ---
        char_to_process = primary_char # Default to primary text
        is_store_operation = False
        if self.shift_active:
            if primary_char in ['A', 'B', 'C', 'D', 'E', 'F']:
                is_store_operation = True
                char_to_process = primary_char # Use A, B, etc. for storage logic
            else:
                # Use the shifted function/text if available, otherwise use primary
                char_to_process = self.shift_map.get(primary_char, primary_char)

        # --- Shift + Variable Assignment ---
        if is_store_operation:
            if self.shift_active and char_to_process in self.variables and char_to_process != 'Ans' and char_to_process != 'x':
                self.variables[char_to_process] = self.last_result # Store last result
                print(f"Stored {self.last_result} into variable {char_to_process}")
                self.toggle_shift() # Deactivate shift after assignment
                # Keep display state disabled after assignment
                self.display.configure(state="disabled")
                return # Stop further processing for this button press

        # --- Normal button press handling (using char_to_process) ---
        self.display.configure(state="normal") # Allow editing / cursor visibility
        current_text = self.display.get("0.0", "end-1c")
        cursor_pos = self.display.index(ctk.INSERT) # Get current cursor position

        disable_display_after = True # Flag to control if display is disabled at the end

        # --- Control Keys (AC, DEL, ON, EXE, Settings, SHIFT, Navigation, INS) ---
        if primary_char == 'ON':
            self.destroy()
            return # Exit immediately
        elif primary_char == 'AC':
            self.display.delete("0.0", "end")
            self.display.insert("0.0", "")
            if self.shift_active: self.toggle_shift()
            # AC should leave cursor at start, but disable display for next input
        elif primary_char == 'DEL':
            # --- Refined DEL logic (Basic Backspace at cursor) ---
            current_cursor_index = self.display.index(ctk.INSERT)
            if current_cursor_index != "1.0":
                # TODO: Add logic to delete multi-char functions like 'sin(' smartly
                self.display.delete(f"{current_cursor_index}-1c", current_cursor_index)
            # If DEL is pressed when text is "0", do nothing special yet
            # Keep display enabled after DEL to allow further editing/deletion
            disable_display_after = False
        elif primary_char == 'EXE': # Removed '=' from this condition
            # --- Auto-close parentheses ---
            open_paren_count = current_text.count('(')
            close_paren_count = current_text.count(')')
            if open_paren_count > close_paren_count:
                missing_parens = ')' * (open_paren_count - close_paren_count)
                current_text += missing_parens
                print(f"Auto-added closing parentheses: {missing_parens}") # Optional: Log this action
            # --- End Auto-close ---

            result = self.calculate(current_text)
            self.display.delete("0.0", "end")
            self.display.insert("0.0", str(result))
            # Update last_result only if calculation was successful and numerical
            if isinstance(result, (int, float, Number)):
                 self.last_result = result
                 self.variables['Ans'] = result # Update Ans variable
            elif isinstance(result, str) and "Error" not in result:
                 # Handle symbolic results or formatted equation results if needed
                 # For now, don't update last_result for non-numerical strings
                 pass
            if self.shift_active: self.toggle_shift()
            # Disable after calculation
        elif primary_char == 'SETTINGS':
            self.angle_mode = "RAD" if self.angle_mode == "DEG" else "DEG"
            self.update_mode_label()
            print(f"Angle mode changed to: {self.angle_mode}")
            self.display.configure(state="disabled") # Keep disabled after settings change
            return
        elif primary_char == 'SHIFT':
            self.toggle_shift()
            self.display.configure(state="disabled") # Keep disabled after shift toggle
            return
        elif primary_char == 'INS':
            self.toggle_insert_mode()
            self.display.configure(state="disabled") # Keep disabled after INS toggle
            return
        # --- Navigation Keys ---
        elif primary_char in ['↑', '↓', '←', '→', 'HOME', 'OK']:
            if primary_char == '←':
                if cursor_pos != "1.0":
                    self.display.mark_set(ctk.INSERT, f"{cursor_pos}-1c")
            elif primary_char == '→':
                 # Check if cursor is already at the end before moving
                 end_pos = self.display.index("end-1c") # Get actual end position
                 if cursor_pos != end_pos:
                     self.display.mark_set(ctk.INSERT, f"{cursor_pos}+1c")
            elif primary_char == 'HOME':
                 self.display.mark_set(ctk.INSERT, "1.0")
            # ... (Placeholders for ↑, ↓, OK) ...

            # Keep display enabled after navigation to show cursor
            disable_display_after = False
            # We don't return here anymore, let the final state check handle it

        # --- Special Function/Variable Keys ---
        elif char_to_process in ['d/dx', '∫dx', 'solve', 'VARIABLE', 'FUNCTION', 'CATALOG', 'TOOLS', 'FORMAT', 'A', 'B', 'C', 'D', 'E', 'F', 'Ans', 'x', 'y']:
            # Use cursor_pos for insertion position
            insert_pos_for_special = cursor_pos # Use the cursor position

            # If display is "0" and inserting at the beginning, replace "0"
            if current_text == "0" and insert_pos_for_special == "1.0":
                 self.display.delete("1.0", "end")
                 insert_pos_for_special = "1.0" # Reset position after delete

            # Insert variable/Ans/x/y names
            if char_to_process in self.variables or char_to_process in ['A', 'B', 'C', 'D', 'E', 'F', 'x', 'y']:
                self.display.insert(insert_pos_for_special, char_to_process)
            # Insert symbolic function syntax
            elif char_to_process == 'd/dx':
                self.display.insert(insert_pos_for_special, "diff(")
            elif char_to_process == '∫dx':
                self.display.insert(insert_pos_for_special, "integrate(")
            elif char_to_process == 'solve':
                self.display.insert(insert_pos_for_special, "solve(")
            else:
                 # Handle other special keys like VARIABLE, FUNCTION etc. if they insert text
                 print(f"Special key pressed: {char_to_process} (Action pending)")


            disable_display_after = False
            # Return only if it's a non-inserting action (like opening a menu)
            # if char_to_process in ['VARIABLE', 'FUNCTION', ...]: return

        # --- Numbers, Operators, Basic Functions, Parentheses, Equals Sign ---
        else:
            # Use cursor_pos for insertion position
            insert_pos = cursor_pos # Use the cursor position determined earlier

            text_to_insert = "" # Determine what text to insert based on char_to_process

            # If display is "0" and inserting at the beginning, replace "0"
            # unless it's an operator/dot/paren/equals that should follow 0
            if current_text == "0" and insert_pos == "1.0" and \
               char_to_process not in ['+', '-', '×', '÷', '.', '(', ')', '^', '*', '=']: # Added '=' here
                 self.display.delete("1.0", "end")
                 insert_pos = "1.0" # Reset position after delete

            # Determine text_to_insert based on char_to_process
            # Ensure '√' is included here (it already is via the dictionary)
            if char_to_process in ['sin', 'cos', 'tan', 'log', 'ln', 'sqrt', 'asin', 'acos', 'atan', 'diff', 'integrate', 'solve', '³√', 'e^', '10^', '√']: # Added '√' explicitly for clarity, though handled by dict
                 # The dictionary correctly maps '√' to 'sqrt'
                 internal_char = {'√': 'sqrt', '³√': 'root_3', 'e^': 'exp', '10^': 'pow10'}.get(char_to_process, char_to_process)
                 text_to_insert = internal_char + "("
            elif char_to_process == 'x²':
                 text_to_insert = "**2"
            elif char_to_process == 'x³':
                 text_to_insert = "**3"
            elif char_to_process == 'x10^':
                 text_to_insert = "*10**"
            elif char_to_process in ['π', 'e', 'x']:
                 # Insert the character as seen on the button (lowercase e, pi symbol)
                 if char_to_process == 'e':
                     text_to_insert = 'e'
                 elif char_to_process == 'π':
                     text_to_insert = 'π'
                 elif char_to_process == 'x':
                     text_to_insert = 'x'
            elif char_to_process == '(-)':
                 text_to_insert = "-"
            # Handle numbers, operators, dot, parentheses, and equals sign directly
            elif char_to_process in '0123456789.+-×÷()=': # Added '=' here
                 # Prevent inserting '=' if one already exists? (Optional validation)
                 # if char_to_process == '=' and '=' in current_text:
                 #     pass # Do nothing if '=' already present
                 # else:
                 text_to_insert = char_to_process
            else:
                 print(f"Warning: Unhandled char_to_process in insertion block: {char_to_process}")

            # Perform the insertion if text_to_insert is determined
            if text_to_insert:
                 self.display.insert(insert_pos, text_to_insert)

            # Keep display enabled after inserting text
            disable_display_after = False


        # --- Final state update ---
        if disable_display_after:
            self.display.configure(state="disabled")
        else:
            self.display.focus_set()

    # ==============================================================================
    # Calculation Engine
    # ==============================================================================
    def calculate(self, expression):
        """
        Parses and evaluates the mathematical expression using SymPy.
        Handles variable substitution, angle modes, symbolic operations, shifted functions, equations, and errors.
        """
        is_equation = False # Define early for use in exception handling
        try:
            # --- Pre-processing ---
            # Replace π with pi for SymPy compatibility before parsing
            expr_str = expression.strip().replace('×', '*').replace('÷', '/').replace('^', '**').replace('π', 'pi')
            if not expr_str: return 0

            # --- Variable Substitution Preparation ---
            local_sympy_vars = {s.name: s for s in self.sympy_vars}
            valid_variables = {k: v for k, v in self.variables.items() if isinstance(v, (int, float, Number))}
            subs_dict = {s: Number(valid_variables[s.name]) for s in self.sympy_vars if s.name in valid_variables and s.name not in ['x', 'y']}

            # --- Define Local Dictionary for Parsing ---
            # Use custom Function classes and direct SymPy functions/constants
            local_dict = {
                # Constants - Map both 'pi' (from input) and 'E'/'e' to SymPy constants
                "pi": pi,
                "E": E,
                "e": E, # Add lowercase 'e' mapping
                 # Direct Sympy Functions
                "sqrt": sqrt, "ln": ln, "abs": Abs, "exp": exp,
                # Custom Functions (Angle Aware or Specific Logic)
                "log": custom_log10,
                "root_3": custom_root3,
                "pow10": custom_pow10,
                "sin": angle_aware_sin,
                "cos": angle_aware_cos,
                "tan": angle_aware_tan,
                "asin": angle_aware_asin,
                "acos": angle_aware_acos,
                "atan": angle_aware_atan,
                # Symbolic Functions (passed directly - these will be parsed into unevaluated functions)
                "diff": diff, "integrate": integrate, "solve": solve,
                # Symbols (including x, y)
                **local_sympy_vars
            }

            # --- Parsing Configuration ---
            # Re-enable implicit multiplication to handle cases like '9x' inside functions
            transformations = standard_transformations + (implicit_multiplication_application, convert_xor,)

            # --- Equation Handling ---
            is_equation = '=' in expr_str and expr_str.count('=') == 1

            if is_equation:
                # Split into LHS and RHS
                lhs_str, rhs_str = expr_str.split('=', 1)
                # Parse LHS and RHS separately
                lhs_expr = parse_expr(lhs_str, local_dict=local_dict, transformations=transformations, evaluate=False)
                rhs_expr = parse_expr(rhs_str, local_dict=local_dict, transformations=transformations, evaluate=False)

                # Create SymPy Equation object
                equation = Eq(lhs_expr, rhs_expr)

                # Substitute known variables (A-F, Ans)
                equation = equation.subs(subs_dict)

                # Assume solving for 'x' if present
                solve_var = local_sympy_vars.get('x')
                if solve_var and solve_var in equation.free_symbols:
                    result = solve(equation, solve_var)
                    # Format result: solve might return a list
                    if isinstance(result, list):
                        if len(result) == 1:
                            return f"x = {result[0]}" # Display single solution nicely
                        else:
                            return f"x = {result}" # Display list for multiple solutions
                    else: # Handle other possible return types from solve if necessary
                        return f"x = {result}"
                else:
                    # If 'x' is not in the equation, maybe try 'y' or return error?
                    return "Error: No variable (x) to solve for"

            # --- Standard Expression Parsing & Evaluation (if not an equation) ---
            else:
                # Parse the expression, keeping custom and symbolic functions unevaluated initially
                # 'e' and 'pi' in expr_str will be correctly mapped via local_dict
                parsed_expr = parse_expr(expr_str, local_dict=local_dict, transformations=transformations, evaluate=False)

                if not isinstance(parsed_expr, Expr):
                     raise sympy.SympifyError(f"Invalid expression input: {expression}")

                # --- Substitution ---
                substituted_expr = parsed_expr.subs(subs_dict) if hasattr(parsed_expr, 'subs') else parsed_expr

                # --- Evaluation ---
                # Check if the expression is an unevaluated symbolic function call
                is_symbolic_func = isinstance(substituted_expr, (sympy.Derivative, sympy.Integral)) \
                                   or (hasattr(substituted_expr, 'func') and substituted_expr.func in (diff, integrate)) # Removed solve from here

                if is_symbolic_func:
                    # Perform the symbolic operation (diff, integrate)
                    result = substituted_expr.doit()
                # Handle explicit solve() function call if needed (though equation format is preferred)
                elif hasattr(substituted_expr, 'func') and substituted_expr.func is solve:
                     # This handles cases like solve(x**2-4, x) entered directly
                     result = substituted_expr.doit() # doit() works for solve too
                else:
                    # --- Numerical Evaluation using evalf ---
                    # Pass the current angle mode to the evalf context for custom functions
                    result = substituted_expr.evalf(subs={'angle_mode': self.angle_mode})

                    # Check if evalf resulted in a number, otherwise try N() as fallback
                    if not result.is_Number:
                        try:
                            result_n = N(substituted_expr)
                            # Only use N() result if evalf didn't produce a number
                            if not result.is_Number:
                                 result = result_n
                        except Exception as e:
                            print(f"Evalf resulted in non-number, N() failed: {e}")
                            # If still not a number, might be an unresolved symbolic expression
                            # Return the result from evalf (which might be symbolic)
                            pass # Keep the result from evalf

                # --- Check for Division by Zero (zoo) ---
                if result == zoo or result == -zoo:
                    print("Calculation Result: zoo (Division by zero)")
                    return "Division by Zero"

                # Return the final result
                return result

        # --- Error Handling (refined) ---
        except (sympy.SympifyError, SyntaxError, TokenError) as e:
            print(f"Calculation Error (Syntax/Parsing): {type(e).__name__} - {e}")
            # Add more specific checks if needed
            if "invalid syntax" in str(e).lower():
                 # ... (Syntax error checks) ...
                 if is_equation:
                     return "Equation Syntax Error"
            return "Syntax Error"
        except TypeError as e:
            # ... (TypeError checks) ...
            if is_equation:
                return "Equation Error"
            return "Type Error"
        # ... (rest of error handling) ...
        except ZeroDivisionError:
            print("Calculation Error: Division by zero")
            return "Division by Zero"
        except (ValueError, sympy.PoleError) as e: # PoleError can be raised by custom tan
            print(f"Calculation Error (Domain/Pole): {e}")
            return "Math Error"
        except AttributeError as e:
            print(f"Calculation Error (Attribute/Subs): {e}")
            return "Error" # Generic error
        except NameError as e:
            print(f"Calculation Error (Name): {e}")
            return "Undefined Error"
        except Exception as e:
            print(f"Unexpected Error: {type(e).__name__} - {e}")
            if is_equation:
                return "Solve Error"
            # ... (other exception checks) ...
            return "System Error"

# ==============================================================================

# Main Application Execution
# ==============================================================================
if __name__ == "__main__":
    # Entry point for the application
    app = CalculatorApp()
    app.mainloop() # Start the customtkinter event loop
