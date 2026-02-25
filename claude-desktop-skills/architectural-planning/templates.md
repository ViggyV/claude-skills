# Architectural Planning Templates

Detailed templates and examples for creating implementation plans.

## Full Implementation Plan Template

```markdown
# Implementation Plan: [Feature Name]

## Discovered Architecture

**Architecture Pattern**: [Identified pattern - layered, hexagonal, microservices, etc.]
**Primary Language**: [Detected from analysis]
**Key Frameworks**: [Found in dependencies]
**Project Structure**: [How code is organized]

**Similar Features**: [Reference existing similar functionality]
- `path/to/similar/feature.ext` - [How it relates]
- `path/to/another/example.ext` - [Pattern to follow]

## Solution Approach

[High-level approach aligned with discovered patterns]

**Why this approach**:
- Fits existing [architecture pattern] naturally
- Reuses existing [components/utilities]
- Maintains consistency with [similar features]
- Minimizes impact on [affected systems]

**Integration Points**:
- [Existing component 1] - [How solution connects, why this integration point]
- [Existing component 2] - [Connection method, justification]

**New Components Needed**:
- [Component name] - [Responsibility, location, reasoning]
  - Location: `path/to/new/component`
  - Interfaces with: [Existing systems]
  - Pattern reference: [Similar component in codebase]

## Implementation Steps

### Step 1: [Specific, atomic task]
**Files**:
- `path/to/file.ext` (modify)
- `path/to/new-file.ext` (create)

**Action**: [What to change, following which existing pattern]

**Example from codebase**:
```[language]
// Found in path/to/similar-file.ext
[relevant code snippet showing pattern]
```

**Apply pattern**:
```[language]
// New implementation following same pattern
[new code matching the pattern]
```

**Rationale**:
- Follows established pattern from [file:line]
- Maintains consistency with [feature]
- Integrates cleanly with [component]

**Dependencies**: None (can start immediately)

### Step 2: [Next task]
**Files**:
- `path/to/another-file.ext` (modify)

**Action**: [Specific change description]

**Example**: See `existing/file.ext:123-145` for similar implementation

**Rationale**: [Why this approach, what pattern it follows]

**Dependencies**: Requires Step 1 completion

### Step 3: [Testing task]
**Files**:
- `test/path/test-file.ext` (create)

**Action**: Add tests following existing test patterns

**Example from test suite**:
```[language]
// Found in test/similar-feature.ext
[test pattern example]
```

**Coverage**:
- Unit tests for [components]
- Integration tests for [workflows]
- Edge cases: [list specific scenarios]

**Dependencies**: Requires Steps 1-2 completion

## Dependencies & Risks

**External Dependencies**:
- [Library name] v[version] - [Why needed, already in project?]
- [Service name] - [How used, configuration needed?]

**Internal Dependencies**:
- [Module A] - [Required functionality]
- [Module B] - [Integration requirement]

**Potential Risks**:
1. **[Risk description]**
   - **Likelihood**: [High/Medium/Low]
   - **Impact**: [High/Medium/Low]
   - **Mitigation**: [How to address]
   - **Fallback**: [Alternative if issue occurs]

2. **[Another risk]**
   - **Likelihood**: [High/Medium/Low]
   - **Impact**: [High/Medium/Low]
   - **Mitigation**: [Prevention strategy]
   - **Fallback**: [Backup plan]

**Breaking Changes**:
- [Any breaking change]
  - **Affected**: [What breaks]
  - **Migration**: [How to update callers]
  - **Timeline**: [When safe to deploy]

**Performance Impact**:
- [Expected impact on performance]
- [Metrics to monitor]
- [Optimization opportunities]

## Testing Strategy

**Test Location**: [Where tests go based on project structure]
- Unit tests: `test/unit/[module]/`
- Integration tests: `test/integration/`
- E2E tests: `test/e2e/`

**Test Approach**: [Following existing test patterns]

**Unit Tests**:
- Framework: [Detected testing framework]
- Pattern: [How project structures tests]
- Coverage targets:
  - [Component A]: Test [specific behaviors]
  - [Component B]: Test [edge cases]
  - [Utility X]: Test [error handling]

**Integration Tests**:
- Test [integration point 1]
- Test [integration point 2]
- Verify [end-to-end workflow]

**Manual Validation**:
- [ ] [Specific validation step with expected outcome]
- [ ] [Another validation step]
- [ ] [Edge case to manually verify]
- [ ] [Performance check]

**Regression Prevention**:
- Add tests for [known edge cases]
- Verify [existing functionality] still works
- Check [performance benchmarks] unchanged

## Success Criteria

**Functional**:
- [ ] [Feature A] works as specified
- [ ] [Integration B] functions correctly
- [ ] [Edge case C] handled properly

**Technical**:
- [ ] All existing tests pass
- [ ] New tests achieve [X]% coverage
- [ ] No performance regression
- [ ] Code follows project conventions
- [ ] Documentation updated

**Quality**:
- [ ] Code review approved
- [ ] Security review passed (if applicable)
- [ ] Performance benchmarks met
- [ ] No new technical debt introduced

## Rollout Plan

**Phase 1: Development**
1. Implement Steps 1-3
2. Pass all tests
3. Code review

**Phase 2: Testing**
1. Deploy to staging
2. Run integration tests
3. Manual QA verification

**Phase 3: Production**
1. Feature flag enabled for [subset]
2. Monitor [key metrics]
3. Gradual rollout to 100%

**Rollback Procedure**:
If issues occur:
1. [Immediate action to take]
2. [How to revert changes]
3. [Data cleanup if needed]

## Timeline Estimate

- Step 1: [X hours/days] - [Rationale]
- Step 2: [X hours/days] - [Rationale]
- Step 3: [X hours/days] - [Rationale]
- Testing & review: [X hours/days]
- **Total**: [X hours/days]

**Assumptions**:
- No major blockers encountered
- Dependencies available when needed
- Team available for reviews

## Future Considerations

**Potential Enhancements**:
- [Enhancement idea 1] - [Why not now, when appropriate]
- [Enhancement idea 2] - [Future opportunity]

**Technical Debt**:
- [Known shortcut taken] - [Plan to address]
- [Temporary solution] - [Long-term fix needed]

**Monitoring & Maintenance**:
- Watch [metric 1] for [expected behavior]
- Monitor [component] for [potential issues]
- Review [logs] for [error patterns]
```

## Simplified Template (For Small Changes)

```markdown
# Implementation Plan: [Small Feature]

## Approach
[1-2 sentence description]

**Pattern**: Following [existing feature] pattern from `file.ext`

## Changes
1. **`path/to/file.ext`**: [What to modify]
2. **`path/to/test.ext`**: [Test to add]

## Validation
- [ ] [How to verify it works]
- [ ] Existing tests pass

## Timeline
[X hours] - [Quick justification]
```

## Architecture Pattern Examples

### Layered Architecture Plan

```markdown
## Discovered Architecture

**Pattern**: Layered (API → Service → Repository → Model)

**Layers**:
- API Layer: `src/api/controllers/`
- Service Layer: `src/services/`
- Repository Layer: `src/repositories/`
- Model Layer: `src/models/`

## Implementation Steps

### Step 1: Add Domain Model
**File**: `src/models/Product.ts` (create)
**Pattern**: Follow `src/models/User.ts` structure
**Layer**: Model (bottom layer, no dependencies)

### Step 2: Add Repository
**File**: `src/repositories/ProductRepository.ts` (create)
**Pattern**: Follow `src/repositories/UserRepository.ts`
**Layer**: Repository (depends only on Model)
**Integration**: Uses existing database connection from `src/db/connection.ts`

### Step 3: Add Service
**File**: `src/services/ProductService.ts` (create)
**Pattern**: Follow `src/services/UserService.ts`
**Layer**: Service (depends on Repository)
**Integration**: Inject ProductRepository via constructor

### Step 4: Add API Controller
**File**: `src/api/controllers/ProductController.ts` (create)
**Pattern**: Follow `src/api/controllers/UserController.ts`
**Layer**: API (depends on Service)
**Integration**: Uses existing auth middleware from `src/api/middleware/auth.ts`
```

### Microservices Architecture Plan

```markdown
## Discovered Architecture

**Pattern**: Microservices with event-driven communication

**Services**:
- User Service: `services/user/`
- Order Service: `services/order/`
- Payment Service: `services/payment/` (new)

**Communication**: Kafka event bus

## Implementation Steps

### Step 1: Create Service Skeleton
**Directory**: `services/payment/`
**Pattern**: Copy structure from `services/order/`
**Components**:
- API server (Express, like other services)
- Event handlers (Kafka consumers)
- Database (PostgreSQL, same as others)

### Step 2: Define Service Contract
**Files**:
- `services/payment/api/openapi.yaml` (API spec)
- `shared/events/payment-events.ts` (event schemas)
**Pattern**: Follow event schema pattern from `shared/events/order-events.ts`

### Step 3: Implement Event Handlers
**File**: `services/payment/handlers/OrderCreatedHandler.ts`
**Pattern**: Follow `services/order/handlers/UserRegisteredHandler.ts`
**Integration**: Subscribe to Kafka topic `order.created`
```

### Hexagonal Architecture Plan

```markdown
## Discovered Architecture

**Pattern**: Hexagonal/Ports & Adapters

**Structure**:
- Core: `src/core/` (business logic)
- Ports: `src/ports/` (interfaces)
- Adapters: `src/adapters/` (implementations)

## Implementation Steps

### Step 1: Define Core Domain
**File**: `src/core/payment/PaymentService.ts`
**Pattern**: Pure business logic, no external dependencies
**Example**: Follow `src/core/order/OrderService.ts`

### Step 2: Define Ports
**File**: `src/ports/PaymentGatewayPort.ts` (interface)
**Pattern**: Define interface for external dependency
**Example**: Like `src/ports/NotificationPort.ts`

### Step 3: Implement Adapter
**File**: `src/adapters/stripe/StripePaymentAdapter.ts`
**Pattern**: Implements PaymentGatewayPort interface
**Example**: Follow `src/adapters/sendgrid/SendGridAdapter.ts`
**Integration**: Inject into PaymentService via dependency injection
```

## Common Planning Scenarios

### Adding New API Endpoint

```markdown
## Plan: Add GET /api/products/:id

**Similar endpoint**: `src/api/users.ts:45-67` (GET /api/users/:id)

### Steps
1. Add route in `src/api/products.ts`
2. Add controller method `ProductController.getById()`
3. Call `ProductService.findById()` (already exists)
4. Add request/response DTOs in `src/dto/product/`
5. Add validation middleware using `express-validator` (like users endpoint)
6. Add tests in `test/api/products.test.ts`

**Differences from users endpoint**:
- Products have SKU field (validate format)
- Include inventory data in response
```

### Database Schema Migration

```markdown
## Plan: Add products table

**Pattern**: Follow existing migration in `migrations/001_create_users.sql`

### Steps
1. Create migration `migrations/003_create_products.sql`
2. Define schema following project conventions:
   - `id` SERIAL PRIMARY KEY
   - `created_at` TIMESTAMP (like all tables)
   - `updated_at` TIMESTAMP (like all tables)
   - Add indexes on frequently queried columns
3. Create down migration for rollback
4. Add model in `src/models/Product.ts`
5. Run migration on dev: `npm run migrate:up`
6. Verify schema: `npm run migrate:status`

**Rollback**: `npm run migrate:down` if issues
```

### Adding New External Integration

```markdown
## Plan: Integrate Stripe payment gateway

**Pattern**: Follow existing SendGrid integration (`src/integrations/sendgrid/`)

### Steps
1. Add adapter: `src/integrations/stripe/StripeAdapter.ts`
   - Implement PaymentGatewayPort interface
   - Follow error handling from SendGrid adapter
2. Add config: `src/config/stripe.ts`
   - Load API key from environment (like sendgrid)
3. Add dependency injection in `src/di/container.ts`
4. Add tests: `test/integrations/stripe.test.ts`
   - Mock Stripe API (like SendGrid tests)
5. Add retry logic using existing `src/utils/retry.ts`

**Configuration needed**:
- Environment variable: `STRIPE_SECRET_KEY`
- Webhook endpoint for payment events
```
