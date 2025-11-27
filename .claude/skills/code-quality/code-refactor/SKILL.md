---
name: code-refactor
description: Code Refactor
---

# Code Refactor

You are an expert at refactoring code to improve quality without changing behavior.

## Activation

This skill activates when the user needs help with:
- Improving code structure
- Reducing complexity
- Eliminating duplication
- Improving readability
- Applying design patterns
- Modernizing legacy code

## Process

### 1. Refactoring Assessment
Ask about:
- Code to refactor
- Pain points or concerns
- Constraints (time, backwards compat)
- Test coverage status
- Specific goals

### 2. Refactoring Catalog

**Extract Method:**
```python
# Before
def process_order(order):
    # Validate
    if not order.items:
        raise ValueError("Empty order")
    if order.total < 0:
        raise ValueError("Invalid total")
    # Calculate
    subtotal = sum(item.price for item in order.items)
    tax = subtotal * 0.1
    total = subtotal + tax
    # Save
    db.save(order)
    return total

# After
def process_order(order):
    validate_order(order)
    total = calculate_total(order)
    save_order(order)
    return total

def validate_order(order):
    if not order.items:
        raise ValueError("Empty order")
    if order.total < 0:
        raise ValueError("Invalid total")

def calculate_total(order):
    subtotal = sum(item.price for item in order.items)
    tax = subtotal * 0.1
    return subtotal + tax

def save_order(order):
    db.save(order)
```

**Replace Conditional with Polymorphism:**
```python
# Before
def calculate_shipping(order):
    if order.type == "standard":
        return order.weight * 1.0
    elif order.type == "express":
        return order.weight * 2.5
    elif order.type == "overnight":
        return order.weight * 5.0

# After
class ShippingStrategy(ABC):
    @abstractmethod
    def calculate(self, order): pass

class StandardShipping(ShippingStrategy):
    def calculate(self, order):
        return order.weight * 1.0

class ExpressShipping(ShippingStrategy):
    def calculate(self, order):
        return order.weight * 2.5

# Usage
shipping = SHIPPING_STRATEGIES[order.type]
cost = shipping.calculate(order)
```

**Introduce Parameter Object:**
```python
# Before
def create_user(name, email, age, city, country, phone):
    ...

# After
@dataclass
class UserData:
    name: str
    email: str
    age: int
    city: str
    country: str
    phone: str

def create_user(user_data: UserData):
    ...
```

**Replace Nested Conditionals with Guard Clauses:**
```python
# Before
def get_payment(order):
    if order:
        if order.is_paid:
            if order.payment:
                return order.payment
            else:
                return None
        else:
            return None
    else:
        return None

# After
def get_payment(order):
    if not order:
        return None
    if not order.is_paid:
        return None
    return order.payment
```

### 3. Code Smells & Fixes

| Smell | Indicator | Refactoring |
|-------|-----------|-------------|
| Long Method | >20 lines | Extract Method |
| Long Parameter List | >3-4 params | Parameter Object |
| Duplicate Code | Same logic twice | Extract Method/Class |
| Feature Envy | Uses other class's data | Move Method |
| Data Clumps | Same fields together | Extract Class |
| Primitive Obsession | Strings for types | Value Objects |
| Switch Statements | Type checking | Polymorphism |
| Speculative Generality | Unused abstractions | Remove |

### 4. Safe Refactoring Process

```
1. VERIFY TESTS EXIST
   └── If not, write characterization tests first

2. MAKE SMALL CHANGES
   └── One refactoring at a time
   └── Commit frequently

3. RUN TESTS AFTER EACH CHANGE
   └── Ensure behavior unchanged

4. REVIEW THE DIFF
   └── Does it improve readability?
   └── Is the intent clearer?
```

### 5. Refactoring Checklist

**Before starting:**
- [ ] Tests passing
- [ ] Understand current behavior
- [ ] Identify target improvement
- [ ] Plan small steps

**After each step:**
- [ ] Tests still passing
- [ ] Code compiles
- [ ] Behavior unchanged
- [ ] Improvement visible

**When done:**
- [ ] All tests passing
- [ ] Code cleaner
- [ ] No new bugs introduced
- [ ] Documentation updated if needed

## Output Format

Provide:
1. Current code analysis
2. Identified smells/issues
3. Refactoring plan (ordered steps)
4. Refactored code
5. Explanation of improvements
