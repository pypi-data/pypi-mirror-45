

def numinput(title, prompt, default=None, minval=None, maxval=None):
    """ From turtle lib:
    Pop up a dialog window for input of a number.
    Arguments:
    title: is the title of the dialog window,
    prompt: is a text mostly describing what numerical information to input.
    default: default value
    minval: minimum value for imput
    maxval: maximum value for input

    The number input must be in the range minval .. maxval if these are
    given. If not, a hint is issued and the dialog remains open for
    correction. Return the number input.
    If the dialog is canceled,  return None.

    Example:
    >>> numinput("Poker", "Your stakes:", 1000, minval=10, maxval=10000)
    """
    import tkinter as tk
    from tkinter import messagebox, simpledialog
    root = tk.Tk()
    root.withdraw()
    return simpledialog.askfloat(title, prompt, initialvalue=default,
                                 minvalue=minval, maxvalue=maxval)


sname = '_iblrig_test_subject'

weight = numinput(f"{sname}", "Weight (gr):")

print(weight)
