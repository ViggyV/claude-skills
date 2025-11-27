---
name: react-component
description: React Component
---

# React Component

You are an expert at building React components and applications.

## Activation

This skill activates when the user needs help with:
- React component design
- Hooks and state management
- Component patterns
- Performance optimization
- TypeScript with React

## Process

### 1. Component Patterns

```tsx
// Functional component with TypeScript
interface UserCardProps {
  user: User;
  onEdit?: (id: string) => void;
  className?: string;
}

export function UserCard({ user, onEdit, className }: UserCardProps) {
  return (
    <div className={cn("p-4 border rounded", className)}>
      <h3>{user.name}</h3>
      <p>{user.email}</p>
      {onEdit && (
        <button onClick={() => onEdit(user.id)}>Edit</button>
      )}
    </div>
  );
}

// Compound components
interface TabsContextValue {
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

const TabsContext = createContext<TabsContextValue | null>(null);

function Tabs({ children, defaultTab }: { children: ReactNode; defaultTab: string }) {
  const [activeTab, setActiveTab] = useState(defaultTab);
  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      {children}
    </TabsContext.Provider>
  );
}

function TabList({ children }: { children: ReactNode }) {
  return <div role="tablist">{children}</div>;
}

function Tab({ value, children }: { value: string; children: ReactNode }) {
  const context = useContext(TabsContext);
  if (!context) throw new Error("Tab must be within Tabs");
  return (
    <button
      role="tab"
      aria-selected={context.activeTab === value}
      onClick={() => context.setActiveTab(value)}
    >
      {children}
    </button>
  );
}

Tabs.List = TabList;
Tabs.Tab = Tab;
```

### 2. Custom Hooks

```tsx
// Fetch hook
function useFetch<T>(url: string) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const controller = new AbortController();

    async function fetchData() {
      try {
        setLoading(true);
        const res = await fetch(url, { signal: controller.signal });
        if (!res.ok) throw new Error("Failed to fetch");
        const json = await res.json();
        setData(json);
      } catch (err) {
        if (err instanceof Error && err.name !== "AbortError") {
          setError(err);
        }
      } finally {
        setLoading(false);
      }
    }

    fetchData();
    return () => controller.abort();
  }, [url]);

  return { data, loading, error };
}

// Debounce hook
function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);

  return debouncedValue;
}

// Local storage hook
function useLocalStorage<T>(key: string, initialValue: T) {
  const [value, setValue] = useState<T>(() => {
    const stored = localStorage.getItem(key);
    return stored ? JSON.parse(stored) : initialValue;
  });

  useEffect(() => {
    localStorage.setItem(key, JSON.stringify(value));
  }, [key, value]);

  return [value, setValue] as const;
}
```

### 3. State Management

```tsx
// useReducer for complex state
interface State {
  items: Item[];
  loading: boolean;
  error: string | null;
}

type Action =
  | { type: "FETCH_START" }
  | { type: "FETCH_SUCCESS"; payload: Item[] }
  | { type: "FETCH_ERROR"; payload: string }
  | { type: "ADD_ITEM"; payload: Item };

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case "FETCH_START":
      return { ...state, loading: true, error: null };
    case "FETCH_SUCCESS":
      return { ...state, loading: false, items: action.payload };
    case "FETCH_ERROR":
      return { ...state, loading: false, error: action.payload };
    case "ADD_ITEM":
      return { ...state, items: [...state.items, action.payload] };
    default:
      return state;
  }
}

function ItemList() {
  const [state, dispatch] = useReducer(reducer, {
    items: [],
    loading: false,
    error: null,
  });

  useEffect(() => {
    dispatch({ type: "FETCH_START" });
    fetchItems()
      .then((items) => dispatch({ type: "FETCH_SUCCESS", payload: items }))
      .catch((err) => dispatch({ type: "FETCH_ERROR", payload: err.message }));
  }, []);

  // ...
}
```

### 4. Performance Optimization

```tsx
// Memoization
const MemoizedChild = memo(function Child({ data }: { data: Data }) {
  return <div>{data.value}</div>;
});

// useMemo for expensive computations
function ExpensiveComponent({ items }: { items: Item[] }) {
  const sortedItems = useMemo(
    () => items.slice().sort((a, b) => a.value - b.value),
    [items]
  );
  return <List items={sortedItems} />;
}

// useCallback for stable references
function Parent() {
  const [count, setCount] = useState(0);

  const handleClick = useCallback(() => {
    setCount((c) => c + 1);
  }, []);

  return <Child onClick={handleClick} />;
}

// Virtualization for large lists
import { useVirtualizer } from "@tanstack/react-virtual";

function VirtualList({ items }: { items: Item[] }) {
  const parentRef = useRef<HTMLDivElement>(null);
  const virtualizer = useVirtualizer({
    count: items.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 50,
  });

  return (
    <div ref={parentRef} style={{ height: 400, overflow: "auto" }}>
      <div style={{ height: virtualizer.getTotalSize() }}>
        {virtualizer.getVirtualItems().map((row) => (
          <div key={row.key} style={{ transform: `translateY(${row.start}px)` }}>
            {items[row.index].name}
          </div>
        ))}
      </div>
    </div>
  );
}
```

### 5. Form Handling

```tsx
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";

const schema = z.object({
  email: z.string().email("Invalid email"),
  password: z.string().min(8, "Password must be 8+ characters"),
});

type FormData = z.infer<typeof schema>;

function LoginForm() {
  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<FormData>({
    resolver: zodResolver(schema),
  });

  const onSubmit = async (data: FormData) => {
    await login(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register("email")} placeholder="Email" />
      {errors.email && <span>{errors.email.message}</span>}

      <input {...register("password")} type="password" />
      {errors.password && <span>{errors.password.message}</span>}

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? "Loading..." : "Login"}
      </button>
    </form>
  );
}
```

## Output Format

Provide:
1. Component code with TypeScript
2. Custom hooks if needed
3. State management approach
4. Performance considerations
5. Accessibility attributes
