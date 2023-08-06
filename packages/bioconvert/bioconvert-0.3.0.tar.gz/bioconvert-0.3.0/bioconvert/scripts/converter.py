# -*- coding: utf-8 -*-

###########################################################################
# Bioconvert is a project to facilitate the interconversion               #
# of life science data from one format to another.                        #
#                                                                         #
# Authors: see CONTRIBUTORS.rst                                           #
# Copyright © 2018  Institut Pasteur, Paris and CNRS.                     #
# See the COPYRIGHT file for details                                      #
#                                                                         #
# bioconvert is free software: you can redistribute it and/or modify      #
# it under the terms of the GNU General Public License as published by    #
# the Free Software Foundation, either version 3 of the License, or       #
# (at your option) any later version.                                     #
#                                                                         #
# bioconvert is distributed in the hope that it will be useful,           #
# but WITHOUT ANY WARRANTY; without even the implied warranty of          #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the           #
# GNU General Public License for more details.                            #
#                                                                         #
# You should have received a copy of the GNU General Public License       #
# along with this program (COPYING file).                                 #
# If not, see <http://www.gnu.org/licenses/>.                             #
###########################################################################
""".. rubric:: Standalone application dedicated to conversion"""
import argparse
import json
import sys
import colorlog
import bioconvert
from bioconvert import ConvBase
from bioconvert.core import graph
from bioconvert.core import utils
from bioconvert.core.base import ConvMeta
from bioconvert.core.converter import Bioconvert
from bioconvert.core.decorators import get_known_dependencies_with_availability
from bioconvert.core.registry import Registry

_log = colorlog.getLogger(__name__)


def main(args=None):
    registry = Registry()

    if args is None:
        args = sys.argv[1:]

    if not len(sys.argv) == 1:
        # check that the first argument is not a converter in the registry
        if args[0].lower() not in list(registry.get_converters_names()) \
                and "." in args[0]:
            in_ext = utils.get_extension(args[0],remove_compression=True)
            out_ext = utils.get_extension(args[1],remove_compression=True)
            #assign to converter the converter (s) found for the ext_pair = (in_ext, out_ext)
            try:
                converter = registry.get_ext((in_ext, out_ext))
                # for testing the mutiple converter for one extention pair
                # converter = [bioconvert.fastq2fasta.Fastq2Fasta, bioconvert.phylip2xmfa.PHYLIP2XMFA]
            except KeyError:
                converter = []

            # if no converter is found
            if not converter:
                _log.error(
                '\n Bioconvert does not support conversion {} -> {}. \n'
                'Please specify the converter'
                '\n Usage : \n\n'
                '\t bioconvert converter input_file output_file \n '
                '\n To see all the converter : '
                '\n \t bioconvert --help '.format(
                     in_ext,out_ext))

                sys.exit(1)
            # if the ext_pair matches a single converter
            elif len(converter) == 1:
                args.insert(0, converter[0].__name__.lower())
            # if the ext_pair matches multiple converters
            else:

                _log.error("\n Ambiguous extension.\n"
                           "You must specify the right conversion \n "
                           "Choose from: \n "
                           "{}".format("\n".join([c.__name__ for c in converter])))
                sys.exit(1)


    # Set the default level
    bioconvert.logger.level = "ERROR"

    # Changing the log level before argparse is run
    try:
        bioconvert.logger.level = args[args.index("-l") + 1]
    except:
        pass
    try:
        bioconvert.logger.level = args[args.index("--level") + 1]
    except:
        pass

    try:
        bioconvert.logger.level = args[args.index("-v") + 1]
    except:
        pass
    try:
        bioconvert.logger.level = args[args.index("--verbosity") + 1]
    except:
        pass

    allow_indirect_conversion = False
    try:
        args.index("--allow-indirect-conversion")
        allow_indirect_conversion = True
    except:
        pass
    try:
        args.index("-a")
        allow_indirect_conversion = True
    except:
        pass


    arg_parser = argparse.ArgumentParser(prog="bioconvert",
                                         description="""Convertor infer the
                                         formats from the first command. We do
                                         not scan the input file. Therefore
                                         users must ensure that their input
                                         format files are properly
                                         formatted.""",
                                         formatter_class=argparse.RawDescriptionHelpFormatter,
                                         epilog="""
Bioconvert contains tens of converters whose list is available as follows:

    bioconvert --help

Each conversion has its own sub-command and dedicated help. For instance:

    bioconvert fastq2fasta --help

Because the subcommand contains the format, extensions are not important
for the conversion itself. This would convert the test.txt file (fastq
format) into a fasta file:

    bioconvert fastq2fasta test.txt test.fasta

Users must ensure that their input format files are properly formatted.

If there is a conversion from A to B and another for B to C, you can also
perform indirect conversion using -a argument (experimental). This command
shows all possible indirect conversions:

    bioconvert --help -a

Please visit http://bioconvert.readthedocs.org for more information about the
project or formats available.

Bioconvert is an open source collaborative project. Please feel free to 
join us at https://github/biokit/bioconvert
""")

    subparsers = arg_parser.add_subparsers(help='sub-command help',
                                           dest='converter', )
    max_converter_width = 2 + max([len(in_fmt) for in_fmt, _, _, _ in registry.iter_converters()])

    # show all possible conversion
    for in_fmt, out_fmt, converter, path in \
            sorted(registry.iter_converters(allow_indirect_conversion)):

        sub_parser_name = "{}2{}".format(in_fmt.lower(), out_fmt.lower())

        if converter:
            link_char = '-'
            if len(converter.available_methods) < 1 and converter._library_to_install is None:
                help_details = " (no available methods please see the doc" \
                               " for install the necessary libraries) "
            elif len(converter.available_methods) < 1 and converter._library_to_install is not None:
                help_details = " (no available methods please install {} \n" \
                               "see the doc for more details) ".format(converter._library_to_install)
            else:
                help_details = " (%i methods)" % len(converter.available_methods)
        else :#if path:
            link_char = '~'
            if len(path) == 3:
                help_details = " (w/ 1 intermediate)"
            else:
                help_details = " (w/ %i intermediates)" % (len(path) - 2)

        help_text = '{}to{}> {}{}'.format(
            (in_fmt + ' ').ljust(max_converter_width, link_char),
            link_char,
            out_fmt,
            help_details,
        )
        sub_parser = subparsers.add_parser(
            sub_parser_name,
            help=help_text,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            # aliases=["{}_to_{}".format(in_fmt.lower(), out_fmt.lower()), ],
            epilog="""Bioconvert is an open source collaborative project. 
Please feel free to join us at https://github/biokit/bioconvert
""",
        )

        if converter:
            converter.add_argument_to_parser(sub_parser=sub_parser)
        elif path:
            for a in ConvBase.get_common_arguments():
                a.add_to_sub_parser(sub_parser)

    arg_parser.add_argument("-v", "--verbosity",
                            default=bioconvert.logger.level,
                            help="Set the outpout verbosity.",
                            choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                            )

    arg_parser.add_argument("--dependency-report",
                            action="store_true",
                            default=False,
                            help="Output all bioconvert dependencies in json and exit")

    arg_parser.add_argument("-a", "--allow-indirect-conversion",
                            action="store_true",
                            help="Show all possible indirect conversions "
                                 "(labelled as intermediate) (EXPERIMENTAL)")

    arg_parser.add_argument("--version",
                            action="store_true",
                            default=False,
                            help="Show version")

    arg_parser.add_argument("--conversion-graph",
                            nargs="?",
                            default=None,
                            choices=["cytoscape", "cytoscape-all", ],
                            )

    try:
        args = arg_parser.parse_args(args)
    except SystemExit as e:
        # parsing ask to stop, maybe a normal exit
        if e.code == 0:
            raise e
        # Parsing failed, trying to guess converter
        from bioconvert.core.levenshtein import wf_levenshtein as lev
        sub_command = None
        args_i = 0
        while sub_command is None and args_i < len(args):
            if args[args_i][0] != '-' and (
                    args_i == 0
                    or args[args_i - 1] != '-v'
                    and args[args_i - 1] != '--verbose'
                    and args[args_i - 1] != '--conversion-graph'
            ):
                sub_command = args[args_i]
            args_i += 1

        if sub_command is None:
            # No sub_command found, so letting the initial exception be risen
            raise e

        conversions = []
        for in_fmt, out_fmt, converter, path in registry.iter_converters(allow_indirect_conversion):
            conversion_name = "{}2{}".format(in_fmt.lower(), out_fmt.lower())
            conversions.append((lev(conversion_name, sub_command), conversion_name))
        matches = sorted(conversions)[:5]
        if matches[0][0] == 0:
            # sub_command was ok, problem comes from elswhere
            raise e
        arg_parser.exit(
            e.code,
            '\n\nYour converter {}() was not found. \n'
            'Here is a list of possible matches: {} ... '
            '\nYou may also add the -a argument to enfore a '
            'transitive conversion. The whole list is available using\n\n'
            '    bioconvert --help -a \n'.format(
                 sub_command, ', '.join([v for _, v in matches]))
        )


    if args.version:
        print("{}".format(bioconvert.version))
        sys.exit(0)

    if args.dependency_report:
        print(json.dumps(get_known_dependencies_with_availability(as_dict=True), sort_keys=True, indent=4, ))
        sys.exit(0)

    if args.conversion_graph:
        if args.conversion_graph.startswith("cytoscape"):
            all_converter = args.conversion_graph == "cytoscape-all"
            print(json.dumps(
                graph.create_graph_for_cytoscape(all_converter=all_converter),
                indent=4,
            ))
        sys.exit(0)

    if args.converter is None:
        msg = 'No converter specified. You can list converter by doing bioconvert --help'
        arg_parser.error(msg)

    if not (getattr(args, "show_methods", False) or args.input_file):
        arg_parser.error('Either specify an input_file (<INPUT_FILE>) or '
                         'ask for available methods (--show-method)')

    if not args.allow_indirect_conversion and \
        ConvMeta.split_converter_to_format(args.converter) not in registry:

        arg_parser.error('The conversion {} is not available directly, '
                         'you have to accept that we chain converter to do'
                         ' so (--allow-indirect-conversion or -a)'.format(args.converter))

    args.raise_exception = args.raise_exception or args.verbosity == "DEBUG"

    # Set the logging level
    bioconvert.logger.level = args.verbosity

    # Figure out whether we have several input files or not
    # Are we in batch mode ?
    import glob
    if args.batch:
        filenames = glob.glob(args.input_file)
    else:
        filenames = [args.input_file]

    for filename in filenames:
        args.input_file = filename
        try:
            analysis(args)
        except Exception as e:
            if args.raise_exception:
                raise e
            else:
                bioconvert.logger.error(e)
            sys.exit(1)


def analysis(args):
    in_fmt, out_fmt = ConvMeta.split_converter_to_format(args.converter)

    # do we want to know the available methods ? If so, print info and quit
    if getattr(args, "show_methods", False):
        class_converter = Registry()[(in_fmt, out_fmt)]
        print("Methods available: {}".format(class_converter.available_methods))
        print("\nPlease see http://bioconvert.readthedocs.io/en/master/"
              "references.html#{} for details ".format(str(class_converter).split("'")[1]))
        if args.raise_exception:
            return
        sys.exit(0)

    # Input and output filename
    infile = args.input_file
    if args.output_file is None and infile:
        outext = ConvMeta.split_converter_to_format(args.converter)
        outfile = infile.rsplit(".", 1)[0] + "." + outext[1].lower()
    else:
        outfile = args.output_file

    # Call a generic wrapper of all available conversion
    conv = Bioconvert(
        infile,
        outfile,
        in_fmt=in_fmt,
        out_fmt=out_fmt,
        force=args.force,
    )

    # # Users may provide information about the input file.
    # # Indeed, the input may be a FastQ file but with an extension
    # # that is not standard. For instance fq instead of fastq
    # # If so, we can use the --input-format fastq to overwrite the
    # # provided filename extension

    # no need to do this
    # if args.input_format:
    #     inext = args.input_format
    #     if not conv.inext.startswith("."):
    #         conv.inext = "." + inext

    if not conv.in_fmt:
        raise RuntimeError("convert infer the format from the extension name."
                           " So add extension to the input file name or use"
                           " --input-format option.")

    if not conv.out_fmt:
        raise RuntimeError("convert infer the format from the extension name."
                           " So add extension to the output file name or use"
                           " --output-format option.")

    bioconvert.logger.info("Converting from {} to {}".format(conv.in_fmt, conv.out_fmt))

    # params = {"threads": args.threads}

    if args.benchmark:
        conv.boxplot_benchmark(N=args.benchmark_N)
        import pylab
        try:pylab.savefig("benchmark_{}.png".format(conv.name))
        except:pylab.savefig("benchmark_{}.png".format(conv.converter.name))
    else:
        # params["method"] = args.method
        conv(**vars(args))


if __name__ == "__main__":
    main()
