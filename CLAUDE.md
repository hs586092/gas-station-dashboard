# Gas Station Dashboard - AI Assistant Guide

## Project Overview

This is a **Gas Station Pricing Strategy Analysis Dashboard** - a single-page web application that helps optimize fuel pricing by analyzing competitor pricing data and correlating it with sales volume data.

**Purpose**: Determine optimal pricing strategies by analyzing the relationship between price differences (relative to competitors) and sales performance using quadratic regression analysis.

**Tech Stack**: Vanilla JavaScript, HTML5, CSS3, Chart.js, PapaParse

## Repository Structure

```
gas-station-dashboard/
├── index.html          # Single-page application (entire codebase)
├── CLAUDE.md          # This file - AI assistant guide
└── .git/              # Git repository
```

**Note**: This is a monolithic single-file application. All HTML, CSS, and JavaScript are contained in `index.html`.

## Architecture

### Single-Page Application Structure

The application follows a traditional three-layer structure within a single file:

1. **HTML (lines 1-398)**: Structure and markup
2. **CSS (lines 9-335)**: Styling and responsive design
3. **JavaScript (lines 399-979)**: Data processing and business logic

### Key Components

#### 1. Data Input Section (lines 342-372)
- Three CSV URL inputs:
  - Gasoline prices (휘발유)
  - Diesel prices (경유)
  - Sales volume (판매량)
- Load button triggers data analysis

#### 2. Analysis Display (lines 374-397)
- Tab-based fuel type selection (Gasoline/Diesel)
- Competitor navigation buttons
- Dynamic analysis sections

#### 3. Visualization Components
- Stat cards for key metrics
- Chart.js scatter plots with regression lines
- Statistical tables with detailed metrics

## Data Model

### Input Data Format

**Price Data (Gasoline/Diesel CSV)**:
```
Date, SLPE, 풍산주유소, 중부주유소, 구산주유소, 만남주유소, 베스트원주유소, 약수터주유소, 유니드주유소, 백제주유소
2024-01-01, 1650, 1680, 1670, ...
```

**Sales Data (PM Copy CSV)**:
```
Date, 휘발유 총판매수량, 휘발유 총건수, 경유 총판매수량, 경유 총건수
2024-01-01, 15000, 250, 12000, 180
```

### Competitors Array
```javascript
const competitors = [
    '풍산주유소', '중부주유소', '구산주유소', '만남주유소',
    '베스트원주유소', '약수터주유소', '유니드주유소', '백제주유소'
];
```

## Core Algorithms

### 1. Quadratic Regression Analysis (lines 773-844)

The application uses **quadratic regression** to model the relationship between price differences and sales:

**Formula**: `y = ax² + bx + c`

Where:
- `x` = Price difference (SLPE price - Competitor price)
- `y` = Sales volume or transaction count
- `a, b, c` = Regression coefficients

**Key Calculations**:
- R² (coefficient of determination): Model fit quality
- Adjusted R²: Accounts for number of parameters
- RMSE (Root Mean Square Error): Prediction accuracy
- Optimal price difference: `-b / (2a)` (vertex of parabola)
- Maximum expected volume: `a × optimal² + b × optimal + c`

### 2. Statistical Metrics (lines 846-864)

**Skewness**: Measures asymmetry of residual distribution
**Kurtosis**: Measures tailedness of residual distribution (excess kurtosis: kurt - 3)

### 3. Price Elasticity Calculation (line 662)

```javascript
const elasticity = (slope × avgPrice) / avgVolume
```

Indicates price sensitivity:
- Negative: Price-sensitive market
- Positive: Price-insensitive market

## Key Functions Reference

### Data Loading
- `loadCSV(url)` (lines 409-418): Async CSV parser using PapaParse
- `loadAndAnalyze()` (lines 420-449): Main entry point, loads all datasets

### Data Processing
- `processData()` (lines 451-459): Orchestrates analysis for both fuel types
- `createCompetitorNav(fuelType)` (lines 461-481): Builds navigation UI
- `analyzeAllCompetitors(fuelType)` (lines 483-501): Processes all competitor data

### Analysis Generation
- `createIntegratedAnalysis(fuelType, priceData)` (lines 503-622):
  - Aggregates data across all competitors
  - Generates combined regression analysis

- `createCompetitorAnalysis(fuelType, competitor, priceData)` (lines 624-771):
  - Individual competitor analysis
  - Calculates price elasticity
  - Generates detailed statistics

### Regression & Statistics
- `performRegression(x, y)` (lines 773-844): Quadratic regression engine
- `calculateSkewness(data)` (lines 846-854): Residual skewness
- `calculateKurtosis(data)` (lines 856-864): Residual kurtosis

### Visualization
- `drawScatterChart(canvasId, x, y, stats, yLabel)` (lines 866-950):
  - Scatter plot with data points
  - Quadratic regression curve
  - Optimal point marker (star)

### UI Control
- `switchFuel(fuelType)` (lines 952-960): Tab switching
- `showAnalysis(fuelType, target)` (lines 962-976): Competitor view switching

## Development Workflows

### Making Changes

1. **Adding New Competitors**
   - Update `competitors` array (line 404)
   - Ensure CSV files include new competitor columns
   - No other changes needed (system is data-driven)

2. **Modifying Statistical Calculations**
   - Main regression logic: `performRegression()` (lines 773-844)
   - Test with sample data before deploying
   - Verify R² and RMSE calculations

3. **Changing Visualization**
   - Chart configuration: `drawScatterChart()` (lines 866-950)
   - Chart.js options: lines 909-948
   - Color scheme: CSS variables or inline styles

4. **UI/UX Improvements**
   - Layout: CSS Grid (lines 183-187, 304-309)
   - Color scheme: Gradient variables (lines 18, 87, 164, 190, 242, 312)
   - Responsive design: Already mobile-friendly via flexbox/grid

### Testing Locally

```bash
# Serve the file locally (Python 3)
python -m http.server 8000

# Or use any static file server
# Then open: http://localhost:8000/index.html
```

### Deployment

This is a static web application requiring:
- Any web server (Apache, Nginx, GitHub Pages, Netlify, Vercel)
- No backend or database
- CORS-enabled CSV sources (Google Sheets, cloud storage)

## Code Conventions

### Naming Conventions
- **Variables**: camelCase (`gasolineData`, `volumeStats`)
- **Functions**: camelCase (`loadAndAnalyze`, `performRegression`)
- **Constants**: camelCase (`competitors`)
- **CSS Classes**: kebab-case (`.stat-card`, `.btn-load`)
- **IDs**: kebab-case with fuel type prefix (`gasoline-nav`, `diesel-content`)

### Code Organization
- **Global State**: Three main data arrays (lines 400-402)
- **Event Handlers**: Inline onclick attributes
- **Chart Instances**: Created dynamically, not stored
- **DOM Manipulation**: Vanilla JavaScript (no frameworks)

### Styling Patterns
- **Color Palette**: Purple gradient (`#667eea`, `#764ba2`)
- **Layout**: Flexbox and CSS Grid
- **Spacing**: Consistent 20px/30px margins
- **Border Radius**: 8-20px for rounded corners
- **Shadows**: Layered box-shadows for depth

## AI Assistant Guidelines

### When Reading Code
1. **File Location**: Everything is in `index.html:1-980`
2. **Language Context**: UI text is in Korean, but variable names are English
3. **No Dependencies**: All libraries loaded via CDN (Chart.js, PapaParse)

### When Making Changes

#### DO:
- ✅ Read the entire `index.html` file first before making changes
- ✅ Preserve the single-file architecture
- ✅ Maintain Korean language UI text
- ✅ Test regression calculations with sample data
- ✅ Keep the existing color scheme unless explicitly asked to change
- ✅ Ensure Chart.js visualizations remain responsive
- ✅ Validate CSV format expectations in comments
- ✅ Use consistent indentation (4 spaces)

#### DON'T:
- ❌ Split into multiple files without explicit request
- ❌ Add build tools/frameworks unless required
- ❌ Change the core regression algorithm without understanding it
- ❌ Remove the integrated analysis (all competitors combined)
- ❌ Break responsive design
- ❌ Add server-side dependencies
- ❌ Change Korean text to English without approval
- ❌ Add unnecessary abstractions to simple code

### Common Tasks

#### Adding a New Metric
1. Calculate in `performRegression()` or new function
2. Add to stats object return value
3. Display in HTML template (stat-card or table row)
4. Update both `createIntegratedAnalysis()` and `createCompetitorAnalysis()`

#### Modifying Regression Model
1. Locate `performRegression()` (lines 773-844)
2. Adjust matrix calculations for different polynomial degree
3. Update vertex calculation for optimal point
4. Update chart label to reflect new formula

#### Changing Data Sources
1. Update input field labels (lines 347-368)
2. Modify column name references in analysis functions
3. Update CSV format documentation in comments

#### Adding Visualizations
1. Add canvas element in HTML template
2. Create Chart.js instance in `drawScatterChart()` or new function
3. Use `setTimeout()` to ensure DOM ready (see line 614)
4. Follow existing chart configuration patterns

### Debug Tips

**Common Issues**:
1. **"Cannot read property of undefined"**: Check CSV column names match code
2. **Charts not rendering**: Verify canvas ID uniqueness and DOM ready state
3. **NaN in calculations**: Validate numeric parsing with `parseFloat()` and `isNaN()`
4. **Empty analysis**: Check date matching between price and sales data

**Debug Points**:
- Line 434-437: Data loading success/failure
- Line 513-516: Date matching logic
- Line 780-788: Regression sum calculations
- Line 812-816: R² calculation

## Mathematical Background

### Why Quadratic Regression?

The relationship between price difference and sales volume follows a **parabolic pattern**:
- When prices are too high: Lost sales to competitors
- When prices are too low: Lower profit margins
- Optimal point exists in between (vertex of parabola)

### Interpreting R²

- **R² > 0.7**: Strong predictive power
- **R² 0.3-0.7**: Moderate relationship
- **R² < 0.3**: Weak correlation (use with caution)

### Adjusted R² vs R²

Adjusted R² penalizes model complexity. Use when comparing different models.

## Security Considerations

### Current Implementation
- ✅ Client-side only (no server vulnerabilities)
- ✅ No user data storage
- ✅ No authentication required
- ✅ Read-only data access

### Potential Risks
- ⚠️ CSV URLs must be CORS-enabled
- ⚠️ No input sanitization (trusted data sources assumed)
- ⚠️ PapaParse dependency (CDN availability)

### Recommendations for Production
1. Validate CSV URLs before loading
2. Sanitize data inputs if accepting user uploads
3. Consider hosting libraries locally for reliability
4. Add error boundaries for failed network requests

## Performance Optimization

### Current Bottlenecks
- Large datasets may slow regression calculations
- Multiple Chart.js instances can impact memory
- DOM manipulation in loops (line 524-537)

### Optimization Strategies
1. **Data Pagination**: Limit analysis to recent N days
2. **Debounce Chart Creation**: Destroy old charts before creating new ones
3. **Web Workers**: Offload regression calculations
4. **Virtual Scrolling**: For large competitor lists

## Version Control

### Git Workflow
- **Main Branch**: `claude/claude-md-mibldfoz9oux1bq9-0153vAAiPpUeCWCCT6H1wib1`
- **Commit Pattern**: Descriptive messages (see git log)
- **Recent Changes**: Multiple iterations updating `index.html`

### Making Commits
```bash
# Stage changes
git add index.html CLAUDE.md

# Commit with descriptive message
git commit -m "Add new competitor analysis feature"

# Push to branch
git push -u origin claude/claude-md-mibldfoz9oux1bq9-0153vAAiPpUeCWCCT6H1wib1
```

## Future Enhancement Ideas

### Potential Features
1. **Export Results**: Download analysis as PDF/Excel
2. **Historical Comparison**: Track optimal price over time
3. **Multi-variate Analysis**: Include weather, day-of-week factors
4. **Automated Recommendations**: AI-powered pricing suggestions
5. **Real-time Data**: Auto-refresh from Google Sheets API
6. **Mobile App**: Progressive Web App (PWA) conversion
7. **A/B Testing**: Compare different pricing strategies
8. **Competitor Benchmarking**: Market position analysis

### Technical Improvements
1. **Module System**: ES6 modules for better organization
2. **TypeScript**: Type safety for complex calculations
3. **Testing**: Unit tests for regression algorithms
4. **Build Process**: Minification and optimization
5. **State Management**: Redux/Zustand for complex state
6. **Accessibility**: ARIA labels and keyboard navigation

## Contact & Resources

### External Dependencies
- **Chart.js**: [chartjs.org](https://www.chartjs.org/) - Visualization library
- **PapaParse**: [papaparse.com](https://www.papaparse.com/) - CSV parser

### Documentation
- Chart.js Docs: https://www.chartjs.org/docs/latest/
- PapaParse Docs: https://www.papaparse.com/docs
- Quadratic Regression: https://en.wikipedia.org/wiki/Polynomial_regression

## Quick Reference

### File Locations
| Feature | Line Range |
|---------|-----------|
| HTML Structure | 1-398 |
| CSS Styles | 9-335 |
| JavaScript Logic | 399-979 |
| Data Loading | 409-449 |
| Regression Engine | 773-844 |
| Visualization | 866-950 |
| UI Controls | 952-976 |

### Key Variables
```javascript
gasolineData    // Gasoline price dataset
dieselData      // Diesel price dataset
salesData       // Sales volume dataset
competitors[]   // Array of 8 competitor names
```

### Important Constants
- Number of competitors: 8
- Regression degree: 2 (quadratic)
- Default timeout for charts: 100ms
- Grid breakpoint: 250px minimum column width

---

**Last Updated**: 2025-11-23
**Version**: 1.0
**Maintainer**: AI Assistant (Claude)
