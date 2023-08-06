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
"""Convert :term:`BAM` format to :term:`BEDGRAPH` formats"""
from bioconvert import ConvBase
import colorlog

from bioconvert.core.decorators import requires

_log = colorlog.getLogger(__name__)


__all__ = ["BAM2BEDGRAPH"]


class BAM2BEDGRAPH(ConvBase):
    """Convert sorted :term:`BAM` file into :term:`BEDGRAPH` file 

    Available methods:

    - bedtools::

        bedtools genomecov -bg -ibam INPUT > OUTPUT


    .. plot::

         from bioconvert.bam2bedgraph import BAM2BEDGRAPH
         from bioconvert import bioconvert_data
         from easydev import TempFile

         with TempFile(suffix=".bed") as fh:
             infile = bioconvert_data("test_measles.sorted.bam")
             convert = BAM2BEDGRAPH(infile, fh.name)
             convert.boxplot_benchmark()


    Note that this BEDGRAPH format is of the form::

        chrom chromStart chromEnd dataValue
    that is contig name, start position, end position, coverage

    .. warning:: the BAM file must be sorted. This can be achieved with
        bamtools.
    """
    _default_method = "bedtools"

    def __init__(self, infile, outfile):
        """
        :param str infile: The path to the input BAM file. **It must be sorted**.
        :param str outfile: The path to the output file
        """
        super().__init__(infile, outfile)


    @requires("bedtools")
    def _method_bedtools(self, *args, **kwargs):
        """
        do the conversion sorted :term`BAM` -> :term:'BEDGRAPH` using bedtools

        :return: the standard output
        :rtype: :class:`io.StringIO` object.
        """
        cmd = "bedtools genomecov -bg -ibam {} > {}".format(self.infile, self.outfile)
        self.execute(cmd)


