// Copyright (c) 2012-2013 Andre Martins
// All Rights Reserved.
//
// This file is part of TurboParser 2.1.
//
// TurboParser 2.1 is free software: you can redistribute it and/or modify
// it under the terms of the GNU Lesser General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// TurboParser 2.1 is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Lesser General Public License for more details.
//
// You should have received a copy of the GNU Lesser General Public License
// along with TurboParser 2.1.  If not, see <http://www.gnu.org/licenses/>.

#include "Parameters.h"
#include <iostream>
#include <math.h>

void Parameters::Save(FILE *fs) {
  weights_.Save(fs);
  labeled_weights_.Save(fs);
}

void Parameters::Load(FILE *fs) {
  weights_.Load(fs);
  labeled_weights_.Load(fs);

  LOG(INFO) << "Squared norm of the weight vector = " << GetSquaredNorm();
  LOG(INFO) << "Number of features = " << Size();
}
