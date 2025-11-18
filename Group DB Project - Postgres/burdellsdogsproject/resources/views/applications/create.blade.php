<!DOCTYPE html>
<html>
<head>
    <title>Apply to Adopt a Dog</title>
</head>
<body>
    <h1>Apply to Adopt a Dog</h1>

    @if ($errors->any())
        <div class="error-list">
            <ul>
                @foreach ($errors->all() as $error)
                    <li>{{ $error }}</li>
                @endforeach
            </ul>
        </div>
    @endif

    <form method="POST" action="{{ route('applications.store') }}">
        @csrf
        
        <div class="form-section">
            <h3>Select a Dog <span class="required">*</span></h3>
            <p>Please select the dog you're interested in adopting:</p>
            
            <div class="dog-selection">
                @if(count($availableDogs) > 0)
                    @foreach($availableDogs as $dog)
                        <div class="dog-card">
                            <input type="radio" id="dog_{{ $dog->dog_id }}" name="dog_id" value="{{ $dog->dog_id }}" required {{ old('dog_id') == $dog->dog_id ? 'checked' : '' }}>
                            <div class="dog-info">
                                <div class="dog-name">{{ $dog->dog_name }}</div>
                                <div>{{ $dog->breeds }}, {{ $dog->sex }}, {{ $dog->age }} years old</div>
                                <div>{{ $dog->description }}</div>
                            </div>
                        </div>
                    @endforeach
                @else
                    <p>No dogs are currently available for adoption.</p>
                @endif
            </div>
        </div>
        
        <div class="form-section">
            <h3>Personal Information</h3>
            
            <div class="form-group">
                <label for="first_name">First Name <span class="required">*</span></label>
                <input type="text" id="first_name" name="first_name" value="{{ old('first_name') }}" required>
            </div>
            
            <div class="form-group">
                <label for="last_name">Last Name <span class="required">*</span></label>
                <input type="text" id="last_name" name="last_name" value="{{ old('last_name') }}" required>
            </div>
            
            <div class="form-group">
                <label for="applicant_email">Email Address <span class="required">*</span></label>
                <input type="email" id="applicant_email" name="applicant_email" value="{{ old('applicant_email') }}" required>
            </div>
            
            <div class="form-group">
                <label for="applicant_phone">Phone Number <span class="required">*</span></label>
                <input type="text" id="applicant_phone" name="applicant_phone" value="{{ old('applicant_phone') }}" required>
            </div>
            
            <div class="form-group">
                <label for="household_size">Household Size (number of people) <span class="required">*</span></label>
                <input type="number" id="household_size" name="household_size" value="{{ old('household_size') }}" min="1" required>
            </div>
        </div>
        
        <div class="form-section">
            <h3>Address Information</h3>
            
            <div class="form-group">
                <label for="street">Street Address <span class="required">*</span></label>
                <input type="text" id="street" name="street" value="{{ old('street') }}" required>
            </div>
            
            <div class="form-group">
                <label for="city">City <span class="required">*</span></label>
                <input type="text" id="city" name="city" value="{{ old('city') }}" required>
            </div>
            
            <div class="form-group">
                <label for="state_abbrev">State <span class="required">*</span></label>
                <input type="text" id="state_abbrev" name="state_abbrev" value="{{ old('state_abbrev') }}" maxlength="2" placeholder="GA" required>
            </div>
            
            <div class="form-group">
                <label for="zip_code">ZIP Code <span class="required">*</span></label>
                <input type="text" id="zip_code" name="zip_code" value="{{ old('zip_code') }}" required>
            </div>
        </div>
        
        <div class="form-group">
            <button type="submit">Submit Application</button>
        </div>
    </form>
</body>
</html>