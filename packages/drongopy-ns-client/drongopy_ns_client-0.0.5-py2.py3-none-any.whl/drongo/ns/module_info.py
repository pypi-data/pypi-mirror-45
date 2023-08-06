"""
modules:
  - name: Authorization and Authentication
    module: auth
    settings:
      definition:
        sections:
          - name: Basic
            properties:
              - name: Auth Secret
                type: string
                widget: da-form-lineinput
                default: drongo.auth.secret
              - name: Token Age (in seconds)
                type: number
                widget: da-form-numberinput
                default: 604800
  - name: Email
    module: email
    settings:
      definition:
        sections:
          - name: Basic
            properties:
              - name: SMTP Host
                type: string
                widget: da-form-lineinput
              - name: SMTP Port
                type: number
                widget: da-form-numberinput
                default: 25
              - name: Username
                type: string
                widget: da-form-lineinput
              - name: Password
                type: string
                widget: da-form-passwordinput
"""
