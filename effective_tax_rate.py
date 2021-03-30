#!/usr/bin/env python3

"""
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 * - Redistributions of source code must retain the above copyright notice, this
 * list of conditions and the following disclaimer.
 *
 * - Redistributions in binary form must reproduce the above copyright notice,
 * this list of conditions and the following disclaimer in the documentation
 * and/or other materials provided with the distribution.
 *
 * - Neither the name of prim nor the names of its contributors may be used to
 * endorse or promote products derived from this software without specific prior
 * written permission.
 *
 * See the NOTICE file distributed with this work for additional information
 * regarding copyright ownership.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
"""

import argparse
import sys

kTaxBrackets = {
  '2020': {
    'single': [
      (0.0, 0.0),
      (9875.0, 0.10),
      (40125.0, 0.12),
      (85525.0, 0.22),
      (163300.0, 0.24),
      (207350.0, 0.32),
      (518400.0, 0.35),
      (float('inf'), 0.37)],
    'joint': [
      (0.0, 0.0),
      (19750.0, 0.10),
      (80250.0, 0.12),
      (171050.0, 0.22),
      (326600.0, 0.24),
      (414700.0, 0.32),
      (622050.0, 0.35),
      (float('inf'), 0.37)]
  },
  '2021': {
    'single': [
      (0.0, 0.0),
      (9950.0, 0.10),
      (40525.0, 0.12),
      (86375.0, 0.22),
      (164925.0, 0.24),
      (209426.0, 0.32),
      (523600.0, 0.35),
      (float('inf'), 0.37)],
    'joint': [
      (0.0, 0.0),
      (19900.0, 0.10),
      (81050.0, 0.12),
      (172750.0, 0.22),
      (329850.0, 0.24),
      (418850.0, 0.32),
      (628300.0, 0.35),
      (float('inf'), 0.37)]
  }
}
kYears = sorted(list(kTaxBrackets.keys()))
kFilings = sorted(list(kTaxBrackets[kYears[0]].keys()))

def main(args):
  assert args.income >= 0.0, 'You can\'t have negative income'
  remaining_income = args.income
  brackets = kTaxBrackets[args.year][args.filing]
  taxes = 0.0
  for bracket_index in range(1, len(brackets)):
    previous_cutoff = brackets[bracket_index - 1][0]
    bracket = brackets[bracket_index]
    cutoff = bracket[0]
    percentage = bracket[1]
    bracket_range = cutoff - previous_cutoff
    print('Bracket ${:.02f}-${:.02f} @ {:.0f}%'.format(
      previous_cutoff, cutoff, percentage * 100))
    print('  Bracket range ${:.02f}'.format(bracket_range))
    amount_in_bracket = min(bracket_range, remaining_income)
    print('  Remaining ${:.02f}'.format(remaining_income))
    print('  Amount in bracket ${:.02f}'.format(amount_in_bracket))
    bracket_tax = amount_in_bracket * percentage
    print('  Tax ${:.02f}'.format(bracket_tax))
    taxes += bracket_tax
    remaining_income -= amount_in_bracket
  assert remaining_income == 0.0, 'Programmer Error :('

  print('')
  print('Year:   {}'.format(args.year))
  print('Filing: {}'.format(args.filing))
  print('Income: ${:.02f}'.format(args.income))
  print('Taxes:  ${:.02f}'.format(taxes))
  print('Rate:   {:.02f}%'.format(taxes / args.income * 100))

if __name__ == '__main__':
  desc = 'Effective Tax Rate Calculator'
  ap = argparse.ArgumentParser(desc)
  ap.add_argument('year', choices=kYears,
                  help='Year of filing')
  ap.add_argument('filing', choices=kFilings,
                  help='Type of filing')
  ap.add_argument('income', type=float,
                  help='Amount of income')
  args = ap.parse_args()
  sys.exit(main(args))
