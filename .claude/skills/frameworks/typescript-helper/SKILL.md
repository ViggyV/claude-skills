---
name: typescript-helper
description: TypeScript Helper
---

# TypeScript Helper

You are an expert at TypeScript development and type system usage.

## Activation

This skill activates when the user needs help with:
- TypeScript types and interfaces
- Generic types
- Type utilities
- Type inference
- TypeScript configuration

## Process

### 1. Type Definitions

```typescript
// Basic types
type ID = string | number;
type Status = "pending" | "active" | "completed";

// Object types
interface User {
  id: ID;
  email: string;
  name: string;
  role: "admin" | "user";
  createdAt: Date;
}

// Optional and readonly
interface Config {
  readonly apiUrl: string;
  timeout?: number;
  headers?: Record<string, string>;
}

// Function types
type Callback<T> = (data: T) => void;
type AsyncFn<T, R> = (input: T) => Promise<R>;

// Index signatures
interface Dictionary<T> {
  [key: string]: T;
}

// Discriminated unions
type Result<T, E = Error> =
  | { success: true; data: T }
  | { success: false; error: E };

function handleResult<T>(result: Result<T>) {
  if (result.success) {
    console.log(result.data); // TypeScript knows data exists
  } else {
    console.error(result.error); // TypeScript knows error exists
  }
}
```

### 2. Generic Types

```typescript
// Generic function
function first<T>(arr: T[]): T | undefined {
  return arr[0];
}

// Generic constraints
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

// Generic class
class Repository<T extends { id: string }> {
  private items: Map<string, T> = new Map();

  save(item: T): void {
    this.items.set(item.id, item);
  }

  find(id: string): T | undefined {
    return this.items.get(id);
  }

  findAll(): T[] {
    return Array.from(this.items.values());
  }
}

// Generic with defaults
interface ApiResponse<T = unknown> {
  data: T;
  status: number;
  message?: string;
}

// Multiple generics
function merge<T, U>(obj1: T, obj2: U): T & U {
  return { ...obj1, ...obj2 };
}
```

### 3. Utility Types

```typescript
// Built-in utilities
type PartialUser = Partial<User>;           // All optional
type RequiredUser = Required<User>;         // All required
type ReadonlyUser = Readonly<User>;         // All readonly
type UserKeys = keyof User;                 // "id" | "email" | "name" | ...
type PickedUser = Pick<User, "id" | "email">;
type OmittedUser = Omit<User, "createdAt">;
type UserRecord = Record<string, User>;

// Custom utility types
type Nullable<T> = T | null;
type Optional<T> = T | undefined;

type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P];
};

type DeepReadonly<T> = {
  readonly [P in keyof T]: T[P] extends object ? DeepReadonly<T[P]> : T[P];
};

// Extract and Exclude
type Numbers = Extract<string | number | boolean, number>;  // number
type NonNumbers = Exclude<string | number | boolean, number>;  // string | boolean

// Return type extraction
type FnReturn = ReturnType<typeof someFunction>;
type ClassInstance = InstanceType<typeof SomeClass>;

// Parameters extraction
type FnParams = Parameters<typeof someFunction>;
```

### 4. Advanced Patterns

```typescript
// Conditional types
type IsArray<T> = T extends any[] ? true : false;
type Flatten<T> = T extends (infer U)[] ? U : T;

// Template literal types
type EventName = `on${Capitalize<string>}`;
type HTTPMethod = "GET" | "POST" | "PUT" | "DELETE";
type Endpoint = `/${string}`;
type Route = `${HTTPMethod} ${Endpoint}`;

// Mapped types with modifiers
type Mutable<T> = {
  -readonly [P in keyof T]: T[P];
};

type Required<T> = {
  [P in keyof T]-?: T[P];
};

// Infer in conditional types
type UnwrapPromise<T> = T extends Promise<infer U> ? U : T;
type ArrayElement<T> = T extends (infer E)[] ? E : never;
type FunctionReturn<T> = T extends (...args: any[]) => infer R ? R : never;

// Builder pattern with types
class QueryBuilder<T extends object> {
  private filters: Partial<T> = {};

  where<K extends keyof T>(key: K, value: T[K]): this {
    this.filters[key] = value;
    return this;
  }

  build(): Partial<T> {
    return this.filters;
  }
}
```

### 5. Type Guards

```typescript
// Type predicate
function isString(value: unknown): value is string {
  return typeof value === "string";
}

function isUser(value: unknown): value is User {
  return (
    typeof value === "object" &&
    value !== null &&
    "id" in value &&
    "email" in value
  );
}

// Assertion function
function assertNonNull<T>(value: T | null | undefined): asserts value is T {
  if (value === null || value === undefined) {
    throw new Error("Value cannot be null or undefined");
  }
}

// Usage
function process(data: unknown) {
  if (isUser(data)) {
    console.log(data.email); // TypeScript knows it's User
  }

  assertNonNull(data);
  // data is now non-null
}
```

### 6. Configuration

```json
// tsconfig.json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "outDir": "./dist",
    "rootDir": "./src",
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

## Output Format

Provide:
1. Type definitions
2. Generic implementations
3. Type utilities
4. Type guards
5. Configuration recommendations
