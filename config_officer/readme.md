# Internal testing block

This documet gives some overview for testing and pipelie

## Testing

Requrements
flake8
```
pip install flake8
pip install black
```

Change with black
```
black config_officer/config_manager.py
```


Testing
```
# Manual
flake8 config_officer/config_manager.py --count --ignore=WPS231,WPS232

# CI
flake8 config_officer/config_manager.py --max-line-length=180 --ignore=WPS231,WPS232
```
