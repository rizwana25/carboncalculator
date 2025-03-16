

// Predefined Emission Factors (kg CO₂/hour)
const predefinedDeviceEmissions = {
    // Bulbs
    'Incandescent Bulb': 0.0285,
    'CFL Bulb': 0.0071,
    'LED Bulb': 0.0048,
    'Fluorescent Tube Light': 0.019,
    'LED Tube Light': 0.0095,
  
    // Fans
    'Conventional Ceiling Fan': 0.0356,
    'BLDC Ceiling Fan': 0.0166,
    'Wall Fan': 0.0238,
    'Table Fan': 0.0285,
  
    // Washing Machines
    'Manual Washing Machine': 0.095,
    'Top Load Washing Machine': 0.2375,
    'Front Load Washing Machine': 0.570,
  // Air Conditioners (Normal ACs)
  '0 Star Normal AC': 0.855,
  '1 Star Normal AC': 0.76,
  '2 Star Normal AC': 0.665,
  '3 Star Normal AC': 0.57,
  '4 Star Normal AC': 0.475,
  '5 Star Normal AC': 0.38,

  // Air Conditioners (Inverter ACs)
  '0 Star Inverter AC': 0.7125,
  '1 Star Inverter AC': 0.6175,
  '2 Star Inverter AC': 0.5225,
  '3 Star Inverter AC': 0.4275,
  '4 Star Inverter AC': 0.3325,
  '5 Star Inverter AC': 0.2375,

  // Refrigerators
  'No Star Refrigerator': 0.0597,
  '1 Star Refrigerator': 0.0529,
  '2 Star Refrigerator': 0.0424,
  '3 Star Refrigerator': 0.0339,
  '4 Star Refrigerator': 0.0272,
  '5 Star Refrigerator': 0.0217,
  
    // Inverters
    '600 VA Inverter': 0.228,
    '800 VA Inverter': 0.304,
    '1000 VA Inverter': 0.38,
    '1500 VA Inverter': 0.57,
  
    // Other Appliances
    'Microwave Oven': 0.285,
    'Desktop Computer': 0.095,
    'Laptop Charging': 0.0285,
    'Phone Charging': 0.0095,
    'Juicer Machine': 0.07125,
    'Iron Box': 0.2375,
    'LPG Stove': 0.2682
};
  // Predefined emission factors for TVs (kg CO₂/hour)
const tvEmissions = {
    Plasma: {
      "15": 0.0713,
      "17": 0.0760,
      "19": 0.0855,
      "24": 0.1045,
      "30": 0.1282,
      "32": 0.1425,
      "37": 0.1805,
      "42": 0.220,
      "50": 0.285
    },
    LED: {
      "15": 0.0071,
      "17": 0.0086,
      "19": 0.0095,
      "24": 0.0114,
      "30": 0.0238,
      "32": 0.0261,
      "37": 0.0285,
      "42": 0.0380,
      "50": 0.0475
    },
    LCD: {
      "15": 0.0086,
      "17": 0.0095,
      "19": 0.0105,
      "24": 0.0190,
      "30": 0.0285,
      "32": 0.0333,
      "37": 0.0380,
      "42": 0.0570,
      "50": 0.0713
    }
  };
  
  // Add predefined device to the list
  document.querySelectorAll('.device-icon').forEach(button => {
    button.addEventListener('click', function () {
      const deviceName = this.getAttribute('data-device');
      const hours = parseFloat(prompt(`Enter usage hours for ${deviceName}:`, "1"));
  
      // Validate input
      if (isNaN(hours) || hours <= 0) {
        alert('Please enter valid hours.');
        return;
      }
  
      const emissionFactor = predefinedDeviceEmissions[deviceName];
      const totalEmissions = (emissionFactor * hours).toFixed(4);
  
      const selectedDevicesList = document.getElementById('selectedDevicesList');
      const deviceItem = document.createElement('div');
      deviceItem.textContent = `${deviceName} - Hours: ${hours}, Emissions: ${totalEmissions} kg CO₂`;
  
      // Add a Remove Button
      const removeButton = document.createElement('button');
      removeButton.textContent = 'Remove';
      removeButton.style.marginLeft = '10px';
      removeButton.addEventListener('click', function () {
        selectedDevicesList.removeChild(deviceItem);
      });
  
      deviceItem.appendChild(removeButton);
      selectedDevicesList.appendChild(deviceItem);
    });

  });
  
  // Show "Other Device" form when "Other" button is clicked
  document.getElementById('otherButton').addEventListener('click', function () {
    const otherDeviceForm = document.getElementById('otherDeviceForm');
    otherDeviceForm.style.display = otherDeviceForm.style.display === 'none' ? 'block' : 'none';
  });
  
  // Add custom device or match predefined device from user input
  document.getElementById('addCustomDevice').addEventListener('click', function () {
    const deviceName = document.getElementById('customDeviceName').value.trim();
    const power = parseFloat(document.getElementById('customPower').value);
    const hours = parseFloat(document.getElementById('customHours').value);
    const selectedDevicesList = document.getElementById('selectedDevicesList');
  
    // Validate inputs
    if (!deviceName || isNaN(hours) || hours <= 0) {
      alert('Please enter valid device details.');
      return;
    }
  
    // Check if device matches predefined appliances
    if (predefinedDeviceEmissions[deviceName]) {
      const emissionFactor = predefinedDeviceEmissions[deviceName];
      const totalEmissions = (emissionFactor * hours).toFixed(4);
  
      const predefinedDeviceItem = document.createElement('div');
      predefinedDeviceItem.textContent = `${deviceName} - Hours: ${hours}, Emissions: ${totalEmissions} kg CO₂`;
  
      const removeButton = document.createElement('button');
      removeButton.textContent = 'Remove';
      removeButton.style.marginLeft = '10px';
      removeButton.addEventListener('click', function () {
        selectedDevicesList.removeChild(predefinedDeviceItem);
      });
  
      predefinedDeviceItem.appendChild(removeButton);
      selectedDevicesList.appendChild(predefinedDeviceItem);
    } else {
      // Calculate emissions for custom devices
      if (isNaN(power) || power <= 0) {
        alert('Please enter a valid power consumption for custom devices.');
        return;
      }
  
      const emissionFactor = 0.475; // Default emission factor (kg CO₂/kWh)
      const totalEmissions = ((power / 1000) * hours * emissionFactor).toFixed(4);
  
      const customDeviceItem = document.createElement('div');
      customDeviceItem.textContent = `${deviceName} - Power: ${power}W, Hours: ${hours}, Emissions: ${totalEmissions} kg CO₂`;
  
      const removeButton = document.createElement('button');
      removeButton.textContent = 'Remove';
      removeButton.style.marginLeft = '10px';
      removeButton.addEventListener('click', function () {
        selectedDevicesList.removeChild(customDeviceItem);
      });
  
      customDeviceItem.appendChild(removeButton);
      selectedDevicesList.appendChild(customDeviceItem);
    }
  
    // Clear the form fields
    document.getElementById('customDeviceName').value = '';
    document.getElementById('customPower').value = '';
    document.getElementById('customHours').value = '';
  });
  // Handle TV type selection and screen size display
document.getElementById('tvType').addEventListener('change', function () {
    const tvSizeSelection = document.getElementById('tvSizeSelection');
    tvSizeSelection.style.display = this.value ? 'block' : 'none';
  });
  
  // Add TV to the selected devices list
  document.getElementById('addTV').addEventListener('click', function () {
    const tvType = document.getElementById('tvType').value;
    const tvSize = document.getElementById('tvSize').value;
    const hours = parseFloat(prompt(`Enter usage hours for ${tvSize} Inch ${tvType} TV:`, "1"));
  
    // Validate inputs
    if (!tvType || !tvSize) {
      alert('Please select both the TV type and screen size.');
      return;
    }
  
    if (isNaN(hours) || hours <= 0) {
      alert('Please enter valid usage hours.');
      return;
    }
  
    // Calculate emissions
    const emissionFactor = tvEmissions[tvType][tvSize];
    const totalEmissions = (emissionFactor * hours).toFixed(4);
  
    // Add TV details to the selected devices list
    const selectedDevicesList = document.getElementById('selectedDevicesList');
    const deviceItem = document.createElement('div');
    deviceItem.textContent = `${tvSize} Inch ${tvType} TV - Hours: ${hours}, Emissions: ${totalEmissions} kg CO₂`;
  
    // Add a Remove Button
    const removeButton = document.createElement('button');
    removeButton.textContent = 'Remove';
    removeButton.style.marginLeft = '10px';
    removeButton.addEventListener('click', function () {
      selectedDevicesList.removeChild(deviceItem);
    });
  
    deviceItem.appendChild(removeButton);
    selectedDevicesList.appendChild(deviceItem);
  
    // Reset the TV dropdowns
    document.getElementById('tvType').value = "";
    document.getElementById('tvSizeSelection').style.display = 'none';
    document.getElementById('tvSize').value = "";
  });