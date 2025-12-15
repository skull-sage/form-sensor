# Smart Form Sensor UI Components

This module provides a user interface for managing and testing semantic text sensors using the backend API.

## Components

### 1. field-list.vue - Sensor Management
**Purpose**: Create and manage text sensors

**Features**:
- **Create New Sensors**: Form to create text sensors with nameId and multi-paragraph text
- **List All Sensors**: Display all existing sensors with their content and paragraph count
- **Delete Sensors**: Remove sensors with confirmation dialog
- **Auto-refresh**: Automatically updates the list when sensors are created/deleted
- **Validation**: Input validation for nameId format and text content

**API Endpoints Used**:
- `GET /text-sensors` - Fetch all sensors
- `POST /create-text-sensor/:nameId` - Create new sensor
- `DELETE /text-sensor/:nameId` - Delete sensor

### 2. field-verify.vue - Text Verification
**Purpose**: Test text similarity against existing sensors

**Features**:
- **Sensor Selection**: Dropdown to choose from available sensors
- **Text Input**: Textarea for entering text to verify
- **Confidence Score**: Visual progress bar and percentage display
- **Color-coded Results**: Green (excellent), Orange (good), Amber (moderate), Red (low)
- **Matched Paragraph**: Shows which paragraph from the sensor matched best
- **Detailed Results**: Expandable section with test details and threshold information

**API Endpoints Used**:
- `GET /text-sensors` - Fetch available sensors for selection
- `POST /text-sensor/:nameId` - Verify text against selected sensor

## Configuration

### API Base URL
Both components use `http://localhost:8000` as the default API base URL. Update the `API_BASE_URL` constant in each component if your backend runs on a different address.

### Confidence Thresholds
The verification component uses the following confidence score interpretations:
- **≥ 80%**: Excellent match (Green)
- **≥ 60%**: Good match (Orange)
- **≥ 40%**: Moderate match (Amber)
- **< 40%**: Low match (Red)

The 60% threshold is used as a reference point for "above/below threshold" status.

## Usage

1. **Creating Sensors**: Use the "Manage Smart Fields" tab to create new text sensors
2. **Testing Text**: Use the "Test Field" tab to verify text against existing sensors
3. **Managing Sensors**: View, create, and delete sensors from the management interface

## Error Handling

Both components include comprehensive error handling:
- Network errors are displayed as notifications
- Validation errors prevent form submission
- Loading states provide user feedback
- Confirmation dialogs prevent accidental deletions

## Styling

Components use Quasar UI framework with:
- Responsive design (mobile-friendly)
- Material Design principles
- Consistent color scheme
- Smooth transitions and hover effects
