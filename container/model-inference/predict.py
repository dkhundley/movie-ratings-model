from InquirerPy import inquirer

def main():
    action = inquirer.select(
        message="Select an action:",
        choices=[
            "Upload",
            "Download",
            "End",
        ],
        default="End",
    ).execute()

    return action


if __name__ == "__main__":
    action = ''
    while action != 'End':
        action = main()
        print(action)