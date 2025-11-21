#!/usr/bin/env python3

import argparse
import subprocess
import sys

def check_command_exists(command):
    try:
        subprocess.run([command, '--version'], check=True, capture_output=True)
        return True
    except FileNotFoundError:
        return False
    except subprocess.CalledProcessError:
        return True

def main():
    parser = argparse.ArgumentParser(description='DevOps utility scripts.')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Check Docker
    if not check_command_exists('docker'):
        print("Error: Docker is not installed. Please install Docker to use this script.")
        sys.exit(1)

    # Check kubectl
    if not check_command_exists('kubectl'):
        print("Error: kubectl is not installed. Please install kubectl to use this script.")
        sys.exit(1)

    # Docker command
    docker_parser = subparsers.add_parser('docker', help='Docker related commands')
    docker_subparsers = docker_parser.add_subparsers(dest='docker_command', help='Docker subcommands')

    docker_build_parser = docker_subparsers.add_parser('build', help='Build a Docker image')
    docker_build_parser.add_argument('image_name', help='The name of the Docker image')
    docker_build_parser.add_argument('--tag', default='latest', help='The tag for the Docker image')
    docker_build_parser.add_argument('--path', default='.', help='The path to the Dockerfile')

    docker_run_parser = docker_subparsers.add_parser('run', help='Run a Docker container')
    docker_run_parser.add_argument('image_name', help='The name of the Docker image')
    docker_run_parser.add_argument('--port', type=int, help='Port mapping (host:container)')

    # Kubernetes command
    k8s_parser = subparsers.add_parser('k8s', help='Kubernetes related commands')
    k8s_apply_parser = k8s_parser.add_parser('apply', help='Apply Kubernetes manifests')
    k8s_apply_parser.add_argument('manifest_file', help='The path to the Kubernetes manifest file')

    args = parser.parse_args()

    if args.command == 'docker':
        if args.docker_command == 'build':
            try:
                subprocess.run(['docker', 'build', '-t', f'{args.image_name}:{args.tag}', args.path], check=True)
                print(f'Docker image {args.image_name}:{args.tag} built successfully.')
            except subprocess.CalledProcessError as e:
                print(f'Error building Docker image: {e}')
                sys.exit(1)
        elif args.docker_command == 'run':
            try:
                command = ['docker', 'run', '-d', args.image_name]
                if args.port:
                    command.extend(['-p', str(args.port) + ':' + str(args.port)])
                subprocess.run(command, check=True)
                print(f'Docker container from image {args.image_name} running in detached mode.')
            except subprocess.CalledProcessError as e:
                print(f'Error running Docker container: {e}')
                sys.exit(1)
        else:
            docker_parser.print_help()
            sys.exit(1)
    elif args.command == 'k8s':
        if args.docker_command == 'apply':
            try:
                subprocess.run(['kubectl', 'apply', '-f', args.manifest_file], check=True)
                print(f'Kubernetes manifests applied from {args.manifest_file}.')
            except subprocess.CalledProcessError as e:
                print(f'Error applying Kubernetes manifests: {e}')
                sys.exit(1)
        else:
            k8s_parser.print_help()
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == '__main__':
    main()