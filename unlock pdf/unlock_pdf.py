import argparse
import configparser
import os
import sys
import pikepdf


def display_banner():
    """Prints a styled program banner to the terminal."""
    banner = """
    ==================================================
               PDF PASSWORD REMOVER UTILITY           
    ==================================================
    * Safely removes encryption & open passwords
    * Retains original file size and quality
    * Accepts CLI arguments or fallback config.ini
    ==================================================
    """
    print(banner)


def get_password_from_config(config_path="config.ini"):
    """Reads the password value from the local configuration file."""
    config = configparser.ConfigParser()

    if not os.path.exists(config_path):
        print(
            f"[-] Error: Configuration file '{config_path}' not found.",
            file=sys.stderr,
        )
        print(
            "[!] Please pass arguments via CLI or create a valid 'config.ini' file.",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        config.read(config_path)
        return config.get("PDF_SETTINGS", "password")
    except (configparser.NoSectionError, configparser.NoOptionError):
        print(
            f"[-] Config Error: Misconfigured '{config_path}' file. Ensure [PDF_SETTINGS] and 'password' are set.",
            file=sys.stderr,
        )
        sys.exit(1)


def remove_pdf_password(input_path, output_path, password):
    """Opens a password-protected PDF and saves it as an unprotected copy."""
    print(f"[*] Processing: '{input_path}'")

    if not os.path.exists(input_path):
        print(
            f"[-] Error: The input file '{input_path}' does not exist.",
            file=sys.stderr,
        )
        return

    try:
        with pikepdf.open(input_path, password=password) as pdf:
            print("[+] Password verified. Decrypting document structure...")
            pdf.save(output_path)

        orig_size = os.path.getsize(input_path)
        new_size = os.path.getsize(output_path)
        print(f"[+] Success! Unprotected PDF saved to '{output_path}'")
        print(f"    - Original Size: {orig_size} bytes")
        print(f"    - Decrypted Size: {new_size} bytes")

    except pikepdf.PasswordError:
        print(
            "[-] Access Denied: The password provided is incorrect.",
            file=sys.stderr,
        )
    except pikepdf.PdfError as e:
        print(
            f"[-] PDF Processing Error: Invalid or corrupt PDF file structure ({e})",
            file=sys.stderr,
        )
    except Exception as e:
        print(f"[-] An unexpected error occurred: {e}", file=sys.stderr)


if __name__ == "__main__":
    display_banner()

    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(
        description="Unlock password-protected PDFs via CLI or config file."
    )
    parser.add_argument(
        "-i", "--input", help="Path to the password-protected input PDF file."
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Path where the unprotected PDF should be saved. (Defaults to input_unprotected.pdf)",
    )
    parser.add_argument(
        "-p",
        "--password",
        help="The password for the PDF. If omitted, the script checks config.ini.",
    )

    args = parser.parse_args()

    # Determine input file (CLI vs Fallback Default)
    input_file = args.input if args.input else "protected_document.pdf"

    # Determine output file name
    if args.output:
        output_file = args.output
    else:
        # Create a logical fallback output filename based on the input filename
        base, ext = os.path.splitext(input_file)
        output_file = f"{base}_unprotected{ext}"

    # Determine password source
    if args.password is not None:
        pdf_password = args.password
        print("[*] Using password provided via command line.")
    else:
        print("[*] No password provided via CLI. Attempting to read config.ini...")
        pdf_password = get_password_from_config()

    # Execute password removal
    remove_pdf_password(input_file, output_file, pdf_password)
