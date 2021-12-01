Fix EXIF for images from WhatsApp
=================================

# Usage

## Prepare environment

- Install virtualenv (if not already there)

    ```
    $ python3 -m pip install --user virtualenv
    ```

- Create virtual environment

    ```
    $ python3 -m venv env
    ```

- Activate virtual environment

    ```
    $ source env/bin/activate
    ```

- Install requirements

    ```
    $ python3 -m pip install -r requirements.txt
    ```

# Run

```
$ python bin/exiffix.py --dp <path to folder>
```

# Source

Implementation based on 
- [WhatsAppBackupFixer](https://holwech.github.io/blog/Fixing-WhatsApp-Backup/)
- [Forum](https://feedback.photoshop.com/conversations/lightroom-classic/lightroom-classic-unable-to-render-some-photos-sent-via-whatsapp-despite-other-apps-being-able-to-open-them/5f5f45f24b561a3d426a1b25)