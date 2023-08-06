import os
import logging

from subprocess import run, CalledProcessError

class ToolMissingError(Exception): pass

class AlignmentPipelineError(Exception): pass


def check_prereqisites(aligner):
    devnull = open(os.devnull, 'w')
    try:
        run(['gunzip', '--help'], stdout=devnull, stderr=devnull, check=True)
        run([aligner, '--help'], stdout=devnull, stderr=devnull, check=True)
        run(['samtools', '--help'], stdout=devnull, stderr=devnull, check=True)
    except FileNotFoundError as e:
        raise ToolMissingError('The alignment pipeline cannot be started because {0} was not found. Is it installed and in the PATH?'.format(e.filename)) from e
    except CalledProcessError as e:
        raise ToolMissingError('The alignment pipeline cannot be started because {0} failed.'.format(" ".join(e.cmd))) from e


def run_alignment(working_dir, genome, reads_path, reads_type, cores, aligner, nanopore):
    """Align full reads with NGMLR or minimap2."""
    check_prereqisites(aligner)
    reads_file_prefix = os.path.splitext(os.path.basename(reads_path))[0]
    full_aln = "{0}/{1}.{2}.querysorted.bam".format(working_dir, reads_file_prefix, aligner)
    if not os.path.exists(full_aln):
        try:
            command = ['set', '-o', 'pipefail', '&&']
            if aligner == "ngmlr":
                # We need to uncompress gzipped files for NGMLR first
                if reads_type == "fasta_gzip" or reads_type == "fastq_gzip":
                    command += ['gunzip', '-c', os.path.realpath(reads_path)]
                    command += ['|', 'ngmlr', '-t', str(cores), '-r', genome]
                    if nanopore:
                        command += ['-x', 'ont']
                else:
                    command += ['ngmlr', '-t', str(cores), '-r', genome, '-q', os.path.realpath(reads_path)]
                    if nanopore:
                        command += ['-x', 'ont']
            elif aligner == "minimap2":
                if nanopore:
                    command += ['minimap2', '-t', str(cores), '-x', 'map-ont', '-a', genome, os.path.realpath(reads_path)]
                else:
                    command += ['minimap2', '-t', str(cores), '-x', 'map-pb', '-a', genome, os.path.realpath(reads_path)]
            command += ['|', 'samtools', 'view', '-b', '-@', str(cores)]
            command += ['|', 'samtools', 'sort', '-n', '-@', str(cores), '-o', full_aln]
            logging.info("Starting alignment pipeline..")
            run(" ".join(command), shell=True, check=True, executable='/bin/bash')
        except CalledProcessError as e:
            raise AlignmentPipelineError('The alignment pipeline failed with exit code {0}. Command was: {1}'.format(e.returncode, e.cmd)) from e
        logging.info("Alignment pipeline finished")
        return full_aln
    else:
        logging.warning("Alignment output file {0} already exists. Skip alignment and use the existing file.".format(full_aln))
        return full_aln