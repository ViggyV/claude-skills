# Frontend Optimizer

You are an expert at optimizing frontend performance.

## Activation

This skill activates when the user needs help with:
- Frontend performance optimization
- Bundle size reduction
- Loading speed improvements
- Core Web Vitals
- Caching strategies

## Process

### 1. Performance Metrics

```
┌─────────────────────────────────────────────────────────────────┐
│                    CORE WEB VITALS                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  LCP (Largest Contentful Paint)     Target: < 2.5s              │
│  └── When main content loads                                     │
│                                                                  │
│  FID (First Input Delay)            Target: < 100ms             │
│  └── Time to interactive                                         │
│                                                                  │
│  CLS (Cumulative Layout Shift)      Target: < 0.1               │
│  └── Visual stability                                            │
│                                                                  │
│  INP (Interaction to Next Paint)    Target: < 200ms             │
│  └── Responsiveness                                              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 2. Code Splitting

```typescript
// Route-based splitting (React)
import { lazy, Suspense } from 'react';

const Dashboard = lazy(() => import('./pages/Dashboard'));
const Settings = lazy(() => import('./pages/Settings'));

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </Suspense>
  );
}

// Component-based splitting
const HeavyChart = lazy(() => import('./components/HeavyChart'));

function Analytics() {
  return (
    <div>
      <h1>Analytics</h1>
      <Suspense fallback={<ChartSkeleton />}>
        <HeavyChart data={data} />
      </Suspense>
    </div>
  );
}

// Dynamic import for libraries
async function loadPdfViewer() {
  const { PDFViewer } = await import('react-pdf');
  return PDFViewer;
}
```

### 3. Image Optimization

```tsx
// Next.js Image
import Image from 'next/image';

function OptimizedImage() {
  return (
    <Image
      src="/hero.jpg"
      alt="Hero image"
      width={1200}
      height={600}
      priority  // For above-fold images
      placeholder="blur"
      blurDataURL={blurDataUrl}
    />
  );
}

// Responsive images
<picture>
  <source
    media="(min-width: 1024px)"
    srcSet="/hero-large.webp"
    type="image/webp"
  />
  <source
    media="(min-width: 768px)"
    srcSet="/hero-medium.webp"
    type="image/webp"
  />
  <img
    src="/hero-small.jpg"
    alt="Hero"
    loading="lazy"
    decoding="async"
  />
</picture>

// Lazy loading with Intersection Observer
function LazyImage({ src, alt }: { src: string; alt: string }) {
  const [isVisible, setIsVisible] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true);
          observer.disconnect();
        }
      },
      { rootMargin: '100px' }
    );

    if (ref.current) observer.observe(ref.current);
    return () => observer.disconnect();
  }, []);

  return (
    <div ref={ref}>
      {isVisible ? <img src={src} alt={alt} /> : <Skeleton />}
    </div>
  );
}
```

### 4. Bundle Optimization

```javascript
// vite.config.js
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom', 'react-router-dom'],
          ui: ['@headlessui/react', '@heroicons/react'],
          charts: ['recharts'],
        },
      },
    },
    sourcemap: true,
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true,
        drop_debugger: true,
      },
    },
  },
});

// webpack.config.js
module.exports = {
  optimization: {
    splitChunks: {
      chunks: 'all',
      cacheGroups: {
        vendor: {
          test: /[\\/]node_modules[\\/]/,
          name: 'vendors',
          chunks: 'all',
        },
      },
    },
    usedExports: true,  // Tree shaking
  },
};

// Import cost reduction
// Bad
import _ from 'lodash';
const sorted = _.sortBy(items, 'name');

// Good
import sortBy from 'lodash/sortBy';
const sorted = sortBy(items, 'name');
```

### 5. Caching Strategies

```typescript
// Service Worker caching
// sw.js
const CACHE_NAME = 'app-v1';
const STATIC_ASSETS = ['/index.html', '/styles.css', '/main.js'];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(STATIC_ASSETS))
  );
});

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((cached) => {
      // Stale-while-revalidate
      const fetched = fetch(event.request).then((response) => {
        const clone = response.clone();
        caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone));
        return response;
      });
      return cached || fetched;
    })
  );
});

// React Query caching
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      gcTime: 30 * 60 * 1000,   // 30 minutes
      refetchOnWindowFocus: false,
    },
  },
});
```

### 6. Performance Monitoring

```typescript
// Web Vitals reporting
import { onCLS, onFID, onLCP, onINP } from 'web-vitals';

function sendToAnalytics(metric: Metric) {
  const body = JSON.stringify({
    name: metric.name,
    value: metric.value,
    id: metric.id,
  });
  navigator.sendBeacon('/analytics', body);
}

onCLS(sendToAnalytics);
onFID(sendToAnalytics);
onLCP(sendToAnalytics);
onINP(sendToAnalytics);

// Performance observer
const observer = new PerformanceObserver((list) => {
  for (const entry of list.getEntries()) {
    console.log(`${entry.name}: ${entry.duration}ms`);
  }
});
observer.observe({ entryTypes: ['measure', 'resource'] });
```

### 7. Optimization Checklist

```markdown
## Performance Checklist

### Loading
- [ ] Code splitting implemented
- [ ] Images optimized and lazy loaded
- [ ] Fonts preloaded
- [ ] Critical CSS inlined
- [ ] Third-party scripts deferred

### Runtime
- [ ] React components memoized
- [ ] Virtual scrolling for long lists
- [ ] Debounced/throttled event handlers
- [ ] Web Workers for heavy computation

### Caching
- [ ] Service Worker configured
- [ ] HTTP cache headers set
- [ ] API responses cached
- [ ] Static assets versioned

### Network
- [ ] Gzip/Brotli compression
- [ ] HTTP/2 enabled
- [ ] CDN configured
- [ ] Preconnect to critical domains
```

## Output Format

Provide:
1. Performance analysis
2. Optimization code
3. Configuration changes
4. Measurement setup
5. Expected improvements
