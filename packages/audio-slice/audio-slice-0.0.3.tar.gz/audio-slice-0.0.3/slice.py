# Script: slice.py
# Author: Kurt Collins (@timesync)
# 
# This script will slice an audio file according specified locations.
# This script use the PyDub package to do the heavy lifting for the audio work.
# You can find that package here: https://github.com/jiaaro/pydub/. In order
# for this script to work with anything but WAV files, though, you will have to
# make sure that either FFmpeg


################################################################################
# Imports
################################################################################

import click
from pydub import AudioSegment


################################################################################
# The main group for the command line interface.
#
#   This segment is contains the main portion of the script execution.
################################################################################

@click.group(invoke_without_command=True)
@click.pass_context
@click.version_option()
@click.argument('filename', 
                type=click.Path(exists=True, dir_okay=False, readable=True))
@click.option('--piece', '-p', 'pieces', type=(float, float), multiple=True)
def cli(ctx, filename, pieces):
    """ A command line utility to slice MP3 files into pieces. """
    if ctx.invoked_subcommand is None and len(pieces) > 0:
        click.echo('Operation - Loading Audio File: %s' % filename)
        audio_file = AudioSegment.from_mp3(filename)

        # Get the slices.
        piece_num = 0
        click.echo('Operation - Slicing and saving.')
        for piece in pieces:
            # Increments
            piece_num += 1

            # Print out the pertinent information.
            click.echo('Current Slice:   %02d' % piece_num)
            click.echo('   Start Time: %6.1f' % piece[0])
            click.echo('     End Time: %6.1f' % piece[1])

            # Get the boundaries of the audio file.
            start = int(piece[0]) * 1000
            end = int(piece[1]) * 1000

            # Get the slice.
            current_slice = audio_file[start:end]

            # Save the slice.
            in_f_name = filename.split('/')[-1][:-4]
            in_f_ext = filename.split('/')[-1][-4:]
            in_f_parent = '/'.join(filename.split('/')[:-1])
            in_f_parent = '.' if in_f_parent == '' else in_f_parent

            out_f_parent = in_f_parent
            out_f_ext = in_f_ext
            out_f_name = '%s-%02d%s' % (in_f_name, piece_num, out_f_ext)

            click.echo('Saving Slice: %s' % (out_f_name))
            current_slice.export('/'.join([out_f_parent, out_f_name]))
        
        click.echo('Operation - Complete')
    elif ctx.invoked_subcommand is None and len(pieces) == 0:
        click.echo('No slices specified; audio file untouched.')
    else:
        click.echo('I am about to invoke %s' % ctx.invoked_subcommand)

