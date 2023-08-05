# Access and Compliance

Access and compliance is a simple Django app to check and verify a
user's acceptance of University of Michigan's Access and Compliance
policy.

## Quick start

1. Add 'django_access_and_compliance' to your `INSTALLED_APPS` setting like this:

```python
    INSTALLED_APPS = [
        'django_access_and_compliance',
        ...
    ]
```

2. Configure the following settings in your application:

```python
# the URL for the desired access and compliance webservice
ACCESS_AND_COMPLIANCE_VALIDATION_URL

# truthy values returned by validation endpoint; e.g. true, yes, etc.
ACCESS_AND_COMPLIANCE_TRUTHY_VALUES
```

## Behavior

This application hooks into an existing Django application and listens for the login signal. Once a user logs in, it makes a request to the `ACCESS_AND_COMPLIANCE_VALIDATION_URL` and checks if the response body matches one of the truthy values specified in `ACCESS_AND_COMPLIANCE_TRUTHY_VALUES`.

After all migrations are performed, the app also ensures that a group called 'Access and Compliance Members' exists.

If the user has attested to the data access and compliance policy, they will be added to the 'Access and Compliance Members' group.

It is up to the application admin to configure any applicable permissions on this group.
